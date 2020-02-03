# Weekly Scrum

**Invitation**: Rashid Waraich, Colin Sheppard (Lawrence Berkeley National Lab)  
**Optional**: Sid Feygin (Stealth Startup, Berkeley Lab alum)  
**Recurring**: Mondays, 10 am PST  

**University Thesis Supervisor**: Prof. Mikhail Itskov, KM, RWTH Aachen University  
**University Advisor**: Markus Hillgärtner, KM, RWTH Aachen University  


## Week 46
 
+ Arrival, onboarding, introduction
+ BEAM/ MatSim 101

## Week 47
 
+ Preliminary tasks discussion
+ Getting BEAM running on local machine, trying configurations for beamville, sf-light experiments
+ Troubleshooting setup problems
+ Introduction to the Calibration problems, getting familiar to old setup, comparing external frameworks 

## Week 48
 
+ Running base setups and comparison between Microsoft Neural Network Intelligence framework/ HyperOpt, raytune framework from RISELab (UC Berkeley)
+ *To be started*: Getting started with setting up BEAM API for external framework  
+ *Scrap*: Polynomial regression with grid search

## Week 49
 
+ [BISTRO paper](http://bistro.its.berkeley.edu/assets/download/pdfs/BISTRO_paper.pdf)
+ Familiarizing oneself with:
    + [Bayesian optimization](http://krasserm.github.io/2018/03/21/bayesian-optimization/)
    + [Extrapolation of learning curves](http://aad.informatik.uni-freiburg.de/papers/15-IJCAI-Extrapolation_of_Learning_Curves.pdf)
+ Technical write up of a problem statement on Overleaf (Conceptual understanding, development of ubiquitous language, all relevant objects identification and their labels etc.)

+ **Overall goals**:
    + Develop a test framework for BEAM.
    + Familiarize oneself with Scala syntax and understand the SigOpt branch.
    + Get SigOpt simulation running, analyze how convergence is achieved.  

## Week 50
 
+ [Ray](https://github.com/ray-project/ray/tree/master/python/ray/tune) - BEAM interface 
    + BayesOpt integration 
    + Early stop (ongoing)

## Week 51
 
+ Parallel Bayesian Optimization with Early stop (Ongoing)

## Week 52
 
+ Parallel Bayesian Optimization with Early stop (Ongoing)

## Week 01
 
+ Out with fever

## Week 02
 
+ Early week (out with fever), Parallel Bayesian with early stop (ongoing). 
    + run sflight1k for 15 iterations on aws
    + early stop criteria at 2nd or 3rd iteration by summing the difference and extrapolating the value PER intercept 

    + early stop mechanism within beam iterations for bohb

## Week 03
 
+ Parallel Bayesian, HyperBand, and BEAM interation_stopper implementaion ongoing.

## Week 04
 
+ Parallel Bayesian, HyperBand, and BEAM interation_stopper implementaion ongoing. 

## Week 05
 
+ [COMPLETED for Beamville] Parallel Bayesian, HyperBand, and BEAM interation_stopper implementaion 
+ Tasks:
    + Modularize the code [COMPLETED for simulation selection]
    + Run sf light on AWS [Ongoing]
    + Compare against nonearly stopping [Not started]
    + Pictorial representation of the whole algorithm [COMPLETED]

## Week 06

+ Available info and resources:
    + 1 run of urbansim-10k for 20 iteration
    + aws (1 x m5a medium) and (1 x m5a large) machine
    + my code doing: bayesian and early stop (based on hard-coded future mode choice iteration values)
+ To do:
    + run urbansim-10k ~100 times 15 iterations to build a database without early stop 
    + start building and test different regression models, verify with cross validation mean squared error 
    + with above step, determine how regression generalizes, if it is linear or nonlinear
    + test my code on urbansim-10k with early stop for 8 workers, 20 beam iterations, 10 bayesian iterations 
    + ETA for this setting should be approx. 6 - 8 hrs or more (?)
 

## Week 07
 
TBD 

## Week 08
 
TBD 

## Week 09
 
TBD 

## Week 10
 
TBD 

## Week 11
 
TBD 

## Week 12
 
TBD 

## Week 13
 
TBD 

## Week 14
 
TBD 

## Week 15
 
TBD 