# TR-FRET_assay_data_analysis
About file format:
1. Raw data file should be a .xlsx file in the default output format of Biotek Synergy Neo2. Otherwise the script will not be able to extract the data correctly.
2. Layout data file should be a .xlsx file with at least two sheets. 
    (1) One of them should store the plate layout information of wells A1 to P24 in cells A1 to X16 and must be named as 'layout'.
    (2) Different compounds in the plate layout should be labeled as different filling colors of the cells. Make sure the compounds are labelled without any duplicate or miss.
    (3) The concentrations of compounds are filled in the cells as cell values. For the blank cells in experiments, it is IMPORTANT to fill in an arbitrary number, unless the blank cells are outside of the processing area (starting row to ending row). Refer to the example_layout.xlsx file.
    (4) Another sheet must be named as 'legend' to store the corresponding compound names for each cell filling color. The compound colors are stored in coloumn 'A' and the compound names in column 'B'. Make sure the colors match those in 'layout' sheet.
