# BLOC Change Experiments

This repository hosts a prototype for coordination analyses using [BLOC](https://github.com/anwala/bloc).

### Prerequisites

* Install BLOC (`cluster` version)
  ```bash
  $ git clone https://github.com/anwala/bloc-coord-experiments.git
  $ cd bloc-coord-experiments/
  $ pip install bloc-cluster/
  ```
* OR install in Docker container
  ```bash
  $ docker run -it --rm --name bloc-coord -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.7-stretch bash
  $ git clone https://github.com/anwala/bloc-coord-experiments.git
  $ cd bloc-coord-experiments/
  $ pip install bloc-cluster/
  ```

### Basic usage

The following command computes pairwise cosine similarity across the BLOC vectors (from action & content words) of all pairs of accounts that were retrieved from Twitter search.

```
$ python bloc-coord-experiments/blc_coord.py --silent -m 10 --bearer-token $BEARER_TOKEN ukraine
```

First, it issues a search query (e.g., "ukraine") to Twitter and extracts a maximum of 100 tweets. Second, it extracts the user IDs (for 10 users - `-m 10`) from the tweets. Third, it extracts a maximum of 100 tweets from the timelines of each user extracted in the previous step and generates BLOC action and content words from the tweets. Finally, it generates TF-IDF vectors from the BLOC words of all users and computes pairwise cosine similarity across all pairs.

The output is written to `pairwise_sim_report.json`. And the runtime (seconds) for extracting tweets, generating BLOC, and computing pairwise similarity is output on the STDOUT.
