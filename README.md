# BLOC Coordination Experiments

This repository hosts a prototype for coordination analyses using [BLOC](https://github.com/anwala/bloc).

### Prerequisites

* Install BLOC (`cluster` version)
  ```bash
  $ git clone https://github.com/anwala/bloc-coord-experiments.git
  $ pip install bloc-coord-experiments/bloc-cluster/
  ```
* OR install in Docker container
  ```bash
  $ docker run -it --rm --name bloc-coord -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.7-stretch bash
  $ git clone https://github.com/anwala/bloc-coord-experiments.git
  $ pip install bloc-coord-experiments/bloc-cluster/
  ```

### Basic usage

The following command computes pairwise cosine similarity across the BLOC vectors (from action & content words) of all pairs of accounts that were retrieved from Twitter search.

```
$ python bloc-coord-experiments/blc_coord.py --silent -m 10 --bearer-token="$BEARER_TOKEN" ukraine
```

<details>
    <summary>Output:</summary>
    
    Done!
    Runtime for extracting tweets: 14.970428
    Runtime for generating BLOC: 0.059710000000000006
    Runtime for pairwise cosine sime: 0.06939816474914551

    Total users: 10
    Total tweets: 912
    Total pairs: 45

    Wrote pairwise_sim_report.json. Preview of first 10 most similar user pairs.
        01. 0.866 Savedemocracyi2, Jojo97223
        02. 0.861 crudeoil1000, jgoldsto
        03. 0.851 Jojo97223, SheilaMacCallum
        04. 0.815 Savedemocracyi2, SheilaMacCallum
        05. 0.793 Savedemocracyi2, Mostrarasesor
        06. 0.721 mccarrennews, SheilaMacCallum
        07. 0.695 Jojo97223, Mostrarasesor
        08. 0.670 Savedemocracyi2, mccarrennews
        09. 0.651 mccarrennews, jgoldsto
        10. 0.617 mccarrennews, Jojo97223
</details>

First, it issues a search query (e.g., "ukraine") to Twitter and extracts a maximum of 100 tweets. Second, it extracts the user IDs (for 10 users - `-m 10`) from the tweets. Third, it extracts a maximum of 100 tweets from the timelines of each user extracted in the previous step and generates BLOC action and content words from their tweets. Finally, it generates TF-IDF vectors from the BLOC words of all users and computes pairwise cosine similarity across all pairs.

The output is written to `pairwise_sim_report.json`. And the runtime (seconds) for extracting tweets, generating BLOC, and computing pairwise similarity is output on the STDOUT.
