
This directory contains outputs from analysis in the form of figures (SVG format preferred), tables (CSV or Parquet preferred).

Additional structure may be used within this directory to compartimentalize analysis steps.

Files should generally contain a "history" of their context in their filename, e.g.:
 - analysis_step1.preprocess_method1.preprocess_method2.csv
 - analysis_step1.preprocess_method1.preprocess_method2.grouping_by_variable1.reduction_method1.csv
 - analysis_step1.preprocess_method1.preprocess_method2.grouping_by_variable1.reduction_method1.statistics.csv
 - analysis_step1.preprocess_method1.preprocess_method2.grouping_by_variable1.reduction_method1.plot_type.svg

🚫 In general, no files in this directory should be added to git history.
