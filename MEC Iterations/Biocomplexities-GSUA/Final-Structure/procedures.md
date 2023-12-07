# How Donald ran the GSUA

# THIS MAY NEED TO BE UPDATED FOR THE STRUCTURE VERSION. 

For this document, anything that is in {curly brackets} is not constant. This means it can be any of the models, inputs, or outputs specified within. This is done with f strings and loops to iterate through every possible combination of charts/analysis to avoid needing to specify which ones to perform. 

Full filepaths are not written, ideally these would not be hardcoded in, but that is just how it is for now, sorry me or other people. `*/` is used to represent the file path into the GSUA folder.

## Generate Samples

* Set the parameters in 'naming_function.py` function 'prob_spec()'for use by SALib
  * Triangular Distributions [min, max, % of that range where the peak is]
  * actual values
    * [5,40,0.54286],      Temperature Peak at 24 
    *  [35,100,0.38461],    Relative Humidity Peak at 60
    *  [330,1300,0.48453],  Atmo CO2 Concentration Peak at 800
    *  [0,1100,0.27273],    PPFD Level Peak at 300
    *  [0,24, 0.66667],    Photoperiod Peak at 16
    *  [0,2]]    Model structure, AMI, BOS, CAV, uniform distribution


## Run 'GSUA script.py'
* begins with clearing the output directories to avoid appending on previous files.
* Calls 'naming_function.py' to generate any model, inputs, outputs, and the problem statement needed.
* Generate the input samples with 'SOBOL_ANALYSIS.SAMPLE()'
  * generates the 896 (equation to describe how that is derived needed) samples used to run the models
  * saves to the file `SOBOL_parameters.txt`
* Read in 'SOBOL_parameters.txt'
* Enters if statements that match which model to run `MEC_{MODEL}_GSUA.RUN_SIM()` matching the simulation structure input for each row of 'SOBOL_parameters.txt'
  * Saves texts files of each individual model to 'GSUA/GSUA_{MODEL}_out/data/GSUA_{MODEL}_data_{OUTPUT}.txt'
  * saves a csv of all outputs/inputs of a single model structure to 'GSUA/GSUA_{MODEL}_out/data/GSUA_{MODEL}_Simulation.csv'

## Analyze the models
* `GSUA_visulization.GSUA_CHARTS()`
  * lines 89-103 generate histograms of the model parameters from the Sobol sampling. 
  * lines 1-172 generate charts of each output for each model on the same charts. Both histograms and scatter plots.
    * saved to `*/GSUA/figures/MEC_Scatter_{INPUT}_X_{OUTPUT}.png`
    * saved to `*/GSUA/figures/MEC_Histogram_{OUTPUT}.png`

  
### Elementary Effects and Sensitivity Analysis 
* Run as `EE.analyze()` in `GSUA_script.py`
  * Defines the model names, inputs, outputs, and problem statement.
  * pull in the output files `GSUA_{MODEL}_Simulations.csv`
  * use the same samples as the sobol analysis
  * Enter the results loop
    * load each output file one at a time by model from `*/GSUA_{MODEL}_out/data/GSUA_{MODEL}_data_{OUTPUT}.txt'`
    * run EE analysis using `problem`, `X`, `Y`, 128 levels (unique levels per input essentially).
    * Save the results to `GSUA/results/full_out/{MODEL}_{OUTPUT}_EE_results.txt` (these outputs are messy)
    * Create a dataframe to clean up the outputs for later use and save to `GSUA/results/EE_out.csv`
* The function `EE.CHART()` is run from `GSUA_script.py`. 
  * Pulls in data from `GSUA/results/EE_out.csv`
  * This creates 4 main types of charts
    * Two with Mu* by sigma with a 1:1 line.
      * Multimodel saved to `GSUA/figures/Elementary_Effects/EE_1-1_{OUTPUT}_multimodel.png`
      * single model saved to `GSUA/GSUA_{MODEL}_out/figures/EE/EE_1-1_{MODEL}_{OUTPUT}.png`
    * Two with mu by sigma with +-2SEM lines
      * Multimodel saved to `GSUA/figures/Elementary_Effects/EE_SEM_{OUTPUT}_multimodel.png`
      * single model saved to `GSUA/GSUA_{MODEL}_out/figures/EE/EE_SEM_{MODEL}_{OUTPUT}.png`

### Sobol Analysis
* run as `SOBOL_ANALYSIS.ANALYZE()` in the `GSUA_script.py`
* pull in the output file `GSUA_{MODEL}_Simulations.csv`
  * parse this file to create individual output files `GSUA_{MODEL}_data_{OUTPUT}.txt`
  * write names of constant outputs to `*/results/constant_outputs.txt`
    * this simply identifies them for easy removal. The file should be deleted before each run otherwise it appends new data with each run. (A future fix if possible)
* Perform Sobol Analysis with SALib functions
  * save messy text file results to `*/results/full_out/{MODEL_OUTPUT}_results.txt`
  * Create dataframes for the S1, S2, and ST effects individually saved to the easier to work with `*/results` as CSV's
* Chart the Sobol results
  * Start with reworking the dataframes. S1 and ST are combined `S1_ST_DF` to be chartable in the same loop since they have the same indexes. S2 is reworked `S2_small_df` to remove the rows of NaN
  * Single model charts first. 
    * first loop charts the S2 results after scanning to correct the error of AMI_ALPHA having results be 0 and conf be NaN.
      * saves outputs to `GSUA/GSUA_{MODEL}_out/figures/sobol/{SOBOL_RESULT}_{MODEL}_{OUTPUT}.png`
    * The next loop iterates through `S1_ST_DF` to create the corresponding charts for S1 and ST results
      * S1 saves outputs to `GSUA/GSUA_{MODEL}_out/figures/sobol/{SOBOL_RESULT}_{MODEL}_{OUTPUT}.png`      
      * ST saves outputs to `GSUA/GSUA_{MODEL}_out/figures/sobol/{SOBOL_RESULT}_{MODEL}_{OUTPUT}.png`


