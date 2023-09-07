# How Donald ran the GSUA

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
* `MEC_MODEL.RUN_SIM()` functions run the selected model version through each set of parameters from `GSUA_parameters.txt`
  * saves compiled results for each model to `GSUA_MODEL_out/data/GSUA_MODEL_Simulation.csv`
* `MEC_MODEL.RUN_CHART()` charts model outputs using output file from `GSUA_MODEL_out/data`
  * generates and saves charts for each model individual model output to `GSUA_MODEL_out/figures`
* `MEC_MODEL.RUN_FULL()` runs both the simulation and charting functions

## Analyze the models

### Sobol Analysis
* pull in the output file `GSUA_MODEL_Simulations.csv`
  * parse this file to create individual output files `GSUA_MODEL_data_OUTPUT.txt`
  * write names of constant outputs to `results/constant_outputs.txt`
    * this simply identifies them for easy removal. The file should be deleted before each run otherwise it appends new data with each run.
* Perform Sobol Analysis with SALib functions
  * save results to `results/MODEL_OUTPUT_results.txt`
* `GSUA_visulization.GSUA_CHARTS()`
  * lines 89-103 generate histograms of the model parameters from the Sobol sampling. 
  * lines 1-172 generate charts of each output for each model on the same charts. Both histograms and scatter plots.
    * saved to `GSUA/figures/MEC_Scatter_INPUT_X_OUTPUT.png`
    * saved to `GSUA/figures/MEC_Histogram_OUTPUT.png`
* Utilize the scatter plots and histograms to identify outputs of interest for sobol analysis
  * this is a painful bit I couldn't automate due to the output structure of the SALib sobol analysis.
  * Take the text files of the files of interest, place into excel to parse/organize the data of interest, copy and paste into the `GSUA_visualization.py` charting functions in lines beyond the main statement.
    * Cry slightly

### Elementary Effects and Sensitivity Analysis 
* Download Simlab, EE measures, and EE Ploting from carpenas site.
* Generate a .fac and .sam with the new sample generation portion of the software. Save to `GSUA/Simlab_files`
  * use the parameters defined in `GSUA script.py` to define the factor parameters.
    * alpha is min, beta is peak, and gamma is the max for the triangular distribution
    * select sobol sampling and 768 samples
  * replace the 768 sample parameters generated in the `.sam` file with those found in the `GSUA_parameters.txt`
  * 