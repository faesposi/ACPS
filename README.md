# ACPS

# Automatic Control Point Search (ACPS) for FreeSurfer brain segmented data 
    The ACPS is designed to imitate the manual placement of control points on FreeSurfer brain segmented data and to help/replace the 
    user in this time-consuming editing

### Prerequisites
    FreeSurfer and Python 2.7.
    Numpy v 1.13


### How to use the ACPS algortihm on your data
    Open the file "init.txt", change the subjects directory (usually your $SUBJETCS_DIR) 
    and the type the name of the subjects in the directory on which the ACPS has to be run.
    Run "launcher.py"
-------------------------------------------------------------------------------------------------------------
      "init.txt" file:
        #Please use this template

        #If you do not want a log please set the value to 0
        1

        #subjects directory
        /home/pippo/freesurfer/subjects

        #name of the subjects to process (if you want to run the ACPS on all the subjects in the directory type '*')
        Sub1
        Sub2
        Sub3
      ----------------------------------------------------------------------------------------------------------

## Authors
    Andrea Gerardo Russo, Eng. PhD candidate
    University of Salerno, Salerno (Italy)
    andrusso@unisa.it
    https://github.com/andreagrusso

## License
Please see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


