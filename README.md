# Technical challenge.


 This command line application first reads user input bouquet design codes, then generates valid bouquets from a user input stream of flowers. 

### Requirements:
- Docker

### Usage:
#### 1. Build docker container 
```
$ docker build --tag flower-challenge . 
```

#### 2. Test sample input
```
$ time cat test/sample_input.txt | docker run -i flower-challenge
AS1a2b
BL2a
AS2a1b
CL1a1b1c1d1e1f1g1h1i
DS1a1b1c1d1e1f1g1h1i1j1k1l1m1n1o1p1q1r1s1t1u1v1w1x1y1z

real	0m2.384s
user	0m0.152s
sys	0m0.024s
```

#### 3. Run
```
$ docker run -i flower-challenge
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
