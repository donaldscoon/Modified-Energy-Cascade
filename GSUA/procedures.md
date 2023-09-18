# How Donald ran the GSUA

For this document, anything that is in {curly brackets} is not constant. This means it can be any of the models, inputs, or outputs specified within. This is done with f strings and loops to iterate through every possible combination of charts/analysis to avoid needing to specify which ones to perform. 

Full filepaths are not written, ideally these would not be hardcoded in, but that is just how it is for now, sorry me or other people. `*/` is used to represent the file path into the GSUA folder.

## Generate Samples

* Set the parameters in `GSUA script.py` for use by SALib
  * Triangular Distributions [min, max, % of that range where the peak is]
  * actual values
    * [[5,40,0.54286],      Temperature Peak at 24 
    *  [35,100,0.38461],    Relative Humidity Peak at 60
    *  [330,1300,0.48453],  Atmo CO2 Concentration Peak at 800
    *  [0,1100,0.27273],    PPFD Level Peak at 300
    *  [0,24, 0.66667]],    Photoperiod Peak at 16
* Use SALib's Sobol sampling function
  * generates the 768 samples used to run the models
  * saves to the file `GSUA_parameters.txt`

## Run the Models
* Split into three sets of functions, all initially commented out. Uncomment the selection you want to use.
* `MEC_{MODEL}_GSUA.RUN_SIM()` functions run the selected model version through each set of parameters from `GSUA_parameters.txt`
  * saves compiled results for each model to `*/GSUA_{MODEL}_out/data/GSUA_{MODE}L_Simulation.csv`
* `MEC_{MODEL}_GSUA.RUN_CHART()` charts model outputs using output file from `*/GSUA_{MODEL}_out/data`
  * generates and saves charts for each model individual model output to `*/GSUA_{MODEL}_out/figures`
* `MEC_{MODEL}_GSUA.RUN_FULL()` runs both the simulation and charting functions

## Analyze the models

### Sobol Analysis
* run as `SOBOL_ANALYSIS.ANALYZE()` in the `GSUA_script.py`
* pull in the output file `GSUA_{MODEL}_Simulations.csv`
  * parse this file to create individual output files `GSUA_{MODEL}_data_{OUTPUT}.txt`
  * write names of constant outputs to `*/results/constant_outputs.txt`
    * this simply identifies them for easy removal. The file should be deleted before each run otherwise it appends new data with each run. (A future fix if possible)
* Perform Sobol Analysis with SALib functions
  * save messy text file results to `*/results/full_out/{MODEL_OUTPUT}_results.txt`
  * Create dataframes for the S1, S2, and ST effects individually saved to the easier to work with `*/results` as CSV's
* `GSUA_visulization.GSUA_CHARTS()`
  * lines 89-103 generate histograms of the model parameters from the Sobol sampling. 
  * lines 1-172 generate charts of each output for each model on the same charts. Both histograms and scatter plots.
    * saved to `*/GSUA/figures/MEC_Scatter_{INPUT}_X_{OUTPUT}.png`
    * saved to `*/GSUA/figures/MEC_Histogram_{OUTPUT}.png`
  
### Elementary Effects and Sensitivity Analysis 
* Run as `MorrisEE.analyze()` in `GSUA_script.py`
  * Defines the model names, inputs, outputs, and problem statement.
  * `analyze()`
    * pull in the output files `GSUA_{MODEL}_Simulations.csv`
    * generate the input samples with the morris method, store in variable `X`. Set to 128 so that the final number of samples matches the outputs of the simulations. (may need to revisit this, see carpena question)
    * Enter the results loop
      * load each output file one at a time from `*/GSUA_{MODEL}_out/data/GSUA_{MODEL}_data_{OUTPUT}.txt'`
      * run morris analysis using `problem`, `X`, `Y`.



# TO DO LIST, after completeing the EE analysis
* Recreate the Sobol charts using automation. 
* Create EE charting functions.
* Package each charting type into a function
  * basic GSUA stuff stays where it is
  * Sobol to sobol function
  * EE to EE function
  
# Questions for Carpena
* Should I use the same samples/model outputs from the python portion to run the EE programs?
  * Right now it appears to generate the inputs in "levels", which appears important.