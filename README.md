# ACPS
## Automatic Control Point Search (ACPS) for FreeSurfer brain segmented data 
ACPS algorithm is designed to imitate the manual placement of control points on FreeSurfer brain segmented data and to help/replace the 
user in this time-consuming editing. The ACPS can be run only on FreeSurfer (v. 5.3) segmented data (after "recon-all" procedure) and
not on T1-weighted raw images.

## Prerequisites
1. FreeSurfer 
2. Python 2.7. :
    - Numpy v 1.13 (or higher)
    - Nibabel
    - Pandas
    - Scikit-learn
    - Xgboost
    


## How to use the ACPS algortihm on your data
Open the file "init.txt" (provided with the code), change the subjects directory (usually your $SUBJETCS_DIR) 
and the type the name of the subjects in the directory on which the ACPS has to be run.
Run from a terminal "launcher.py". It is not compulsory to have the data on wich the ACPS has to 
be run in your $SUBJECTS_DIR. However, because of the FreeSurfer software architecture, to see 
the control points placed by the ACPS (e. g. using "tkmedit") your data must be in the $SUBJECTS_DIR.
 
-------------------------------------------------------------------------------------------------------------
      "init.txt" file:
        #Please use this template

        #subjects directory
        /home/pippo/freesurfer/subjects

        #name of the subjects to process (if you want to run the ACPS on all the subjects in the directory type '*')
        Sub1
        Sub2
        Sub3
      ----------------------------------------------------------------------------------------------------------

## Important notes
This algorithm was specifically developed to imitate as much as possible the human operator in placing 
control points on the FreeSurfer brain segmented data. We recommend to apply the ACPS algorithm on FreeSurfer
segmented data that **STRONGLY NEED** the application of control points and not on your entire subject cohort. 
**Not all FreeSurfer segmented data need control points!** (for a useful description of this editing 
procedure please see https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/ControlPoints_tktools)
Moreover, we **STRONGLY** recommend to quickly check the resulting control points and to remove/add
false/negative positives sample. 
    



## Authors
    Andrea Gerardo Russo, Eng. PhD candidate
    University of Salerno, Salerno (Italy)
    andrusso@unisa.it
    https://github.com/andreagrusso
    
    Antonietta Canna, Eng. PhD candidate
    University of Salerno, Salerno (Italy)
    acanna@unisa.it
    
    Sara Ponticorvo, Eng. PhD candidate
    University of Salerno, Salerno (Italy)
    sponticorvo@unisa.it
    
    Professor Fabrizio Esposito, Eng,  PhD
    University of Salerno, Salerno (Italy)
    faesposi@unisa.it
    https://github.com/faesposi


## License
If you use this work please cite:
**Antonietta Canna, Andrea G. Russo, Sara Ponticorvo, Renzo Manara, Alessandro Pepino, Mario Sansone, Francesco Di Salle, Fabrizio Esposito, Automated search of control points in surface-based morphometry, NeuroImage, Available online 16 April 2018, ISSN 1053-8119, https://doi.org/10.1016/j.neuroimage.2018.04.035.**

Please see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
The Authors thank Michele Fratello (https://github.com/mfratello) for the support provided 
in the development and training of the classifier and for the illuminating discussion on 
machine learning. 



