**1) Confirm Backend is running completely - DONE**

**2) Confirm frontend is running completely using react command - DONE**



### **Tasks:**

1. **Improve the UI**
2. **Check the Legend Part**
3. **Integrate the Legend Part**
4. **Create a dummy PDF for showing translation**
5. **Resolve the frontend Tauri Issue**
6. **Call Prerna - DONE**
7. **Confirm docs with Tanish**





#### **Integrating Legends -** 

1. **Fit it between receiving the translation object, and creating the new PDF in the main process flow.**
2. **Adapt the return object structure of the Chinese to English translation function and/or the input arguments of the legend function.**
3. **? Does the legend file identify between to be or not to be abbreviated text.**
4. **? Legend file needs a average font size from the main process flow. What to do of it?**
5. **? Need a way to identify where to overlay abbreviations and where complete text will go.**
6. **? Have to perform overlaying of English text before legend addition as adding a legend to the PDF would change coordinates, leading to mismatch in bounding box creating**



			**-** Possible solution - break the legend addition process and use specific functions as and when required. 

&nbsp;				- Generate the translations and use the Legend file function identify which texts need abbreviations and, then another to create those 					abbreviations and pass them back to the main process flow.			

				**- Use the returned data object to overlay the PDF with the translated texts and/or the abbreviations received from the Legend file function.**

				**- The Legend file functions parallelly build the legend to be inserted, and when the main process is done overlaying the text, it passes that** 

				**PDF to the Legend file functions  which will add the legend created.**

					**- ? How to synchronize the legend creation in Legend file and text overlaying in the main process flow? Supposedly the legend creation 					is done by one function in the Legend file, then it would need the output of both the processes together.**





* **After Chinese to English translation, to identify the text that needs translation, create a new function -** 
* 
**&nbsp;	- This function identifies which text needs to be abbreviated.**

	**- Implements the abbreviation functionality directly here on those texts.**

	**- Adds the abbreviations into the original data passed.**

	**- And finally returns two data objects -** 

		**- One for legend creation which contains the text that needs to be converted into legend**

		**- A structurally similar data object to input argument, complete with the abbreviations passed to the overlaying function, so that it does not have to 		wait for legend creation, and generate the final pdf, which can then be stitched with the new legend.**

