import argparse
import logging
import osometweet
import time

from argparse import Namespace
from bloc.generator import gen_bloc_for_users
from bloc.subcommands import run_subcommands

from bloc.util import genericErrorInfo
from bloc.util import dumpJsonToFile

def get_generic_args():

    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30), description='Behavioral Language for Online Classification (BLOC) command-line tool')
    parser.add_argument('query', help='Query to issue to Twitter search')

    parser.add_argument('--bearer-token', default='', help='Twitter v2 API bearer token to access API')
    parser.add_argument('-m', '--max-users', type=int, default=10, help='Maximum number of users to generate BLOC and run pairwise BLOC cosine sim. analysis. -1 for no restriction.')
    parser.add_argument('--silent', action='store_true', help='Do not print progress')

    return parser

def get_bloc_params(user_ids, bearer_token, token_pattern='word', no_screen_name=True, account_src='Twitter search', no_sleep=True, max_pages=1, max_results=100, bloc_alphabets = ['action', 'content_syntactic']):
    
    #bloc_alphabets = ['action', 'change', 'content_syntactic', 'content_semantic_entity', 'content_semantic_sentiment']
    
    params = {
        'screen_names_or_ids': user_ids, 
        'bearer_token': bearer_token, 
        'account_src': account_src,
        'account_class': '',
        'access_token': '', 'access_token_secret': '', 'consumer_key': '', 'consumer_secret': '', 
        'blank_mark': 60, 'minute_mark': 5, 'segmentation_type': 'week_number', 'days_segment_count': -1, 
        'ansi_code': '91m', 
        'bloc_alphabets': bloc_alphabets, 'bloc_symbols_file': None, 
        'cache_path': '', 'cache_read': False, 'cache_write': False, 
        'following_lookup': False, 
        'keep_tweets': False, 
        'keep_bloc_segments': False, 
        'log_file': '', 'log_format': '', 'log_level': 'INFO', 'log_dets': {'level': 20},
        'max_pages': max_pages, 'max_results': max_results, 
        'no_screen_name': no_screen_name, 'no_sleep': no_sleep, 
        'output': None, 
        'timeline_startdate': '', 'timeline_scroll_by_hours': None, 'time_function': 'f2', 
        'subcommand': '', 

        'fold_start_count': 4,
        'keep_tf_matrix': False,
        'ngram': 1 if token_pattern == 'word' else 2,
        'sort_action_words': False,#
        'set_top_ngrams': False,
        'tf_matrix_norm': '',
        'token_pattern': token_pattern,
        'top_ngrams_add_all_docs': False,
        'sim_no_summary': True,
        'tweet_order': 'reverse'
    }

    return params, Namespace(**params)

def get_users_for_query(ostwt, query):
    
    obj_fields = osometweet.TweetFields()
    obj_fields.fields = ['author_id']

    try:
        response = ostwt.search( query=query, full_archive_search=False, fields=obj_fields, max_results=100 )
    except:
        genericErrorInfo()
        return []

    author_ids = list(set([ u['author_id'] for u in response['data'] ]))
    return author_ids

def proc_req(args):
    
    ostwt = osometweet.OsomeTweet( osometweet.OAuth2(bearer_token=args.bearer_token, manage_rate_limits=False) )
    user_ids = get_users_for_query(ostwt, args.query)
    gen_bloc_params, gen_bloc_args = get_bloc_params(user_ids, args.bearer_token)


    tweet_fields = osometweet.TweetFields()
    user_fields = osometweet.UserFields()
    expansions = osometweet.TweetExpansions()

    tweet_fields.fields = ['id', 'text', 'source', 'lang', 'created_at', 'entities', 'context_annotations', 'referenced_tweets']
    user_fields.fields = ['public_metrics', 'created_at']
    expansions.expansions = ['author_id', 'in_reply_to_user_id', 'geo.place_id', 'attachments.media_keys', 'referenced_tweets.id', 'referenced_tweets.id.author_id']

    gen_bloc_params['twitter_api_tweet_fields'] = tweet_fields + user_fields
    gen_bloc_params['twitter_api_expansion_fields'] = expansions
    gen_bloc_params['screen_names_or_ids'] = gen_bloc_params['screen_names_or_ids'][:args.max_users] if args.max_users > 0 else gen_bloc_params['screen_names_or_ids']


    bloc_payload = gen_bloc_for_users(**gen_bloc_params)
    runtime_details = bloc_payload.get('runtime_details', {})
    bloc_payload = bloc_payload.get('all_users_bloc', [])
    total_tweets = sum([ user_bloc['more_details']['total_tweets'] for user_bloc in bloc_payload ])

    start_time = time.time()
    pairwise_sim_report = run_subcommands(gen_bloc_args, 'sim', bloc_payload)
    pairwise_comp_time = time.time() - start_time

    print('Done!')
    
    print('Runtime for extracting tweets:', runtime_details['gen_tweets_total_seconds'])
    print('Runtime for generating BLOC:', runtime_details['gen_bloc_total_seconds'])
    print('Runtime for pairwise cosine sime:', pairwise_comp_time)

    print('\nTotal users:', len(gen_bloc_params['screen_names_or_ids']) )
    print('Total tweets:', total_tweets)
    print('Total pairs:', len(pairwise_sim_report))
    
    print('\nWrote pairwise_sim_report.json')
    dumpJsonToFile('pairwise_sim_report.json', pairwise_sim_report)

def main():

    parser = get_generic_args()
    args = parser.parse_args()
    
    if( args.silent is False ):
        logging.basicConfig(format='', level=logging.INFO)
    
    proc_req(args)

if __name__ == '__main__':
    main()
