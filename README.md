# Technical challenge Bloomon.


 This command line application first reads user input bouquet design codes, then generates valid bouquets from a user input stream of flowers. 

### Requirements:
- Docker

### Usage:
#### 1. Build docker container 
```
$ docker build --tag bloomon-challenge . 
```

#### 2. Test sample input
```
$ cat test/sample_input.txt | docker run -i bloomon-challenge
AS1a2b
BL2a
AS2a1b
```

#### 3. Run
```
$ docker run -i bloomon-challenge
$ design1
$ design2
...
$ <empty line>
$ flower1
$ flower2
$ flower3
bouquet1
$ flower4
...
```
