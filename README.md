# ElizabethLineTool
A quick tool to check elizabeth line status instead of googling it - shows the top 5 trains to each unique destination. Time autoadjusts to DST.
Can only be run 50 times per minute due to API restrictions - change the code to add your own access codes if you want to extend it.

The function will be extended to a physical device which updates every 30 seconds and updates it on a EINK/OLED screen which can be hung up in common places in the house. Perfect to always know how close you are to being late.

### How to Use

Just run the script with python or just change the location in the `lizzy.bat` file to your repo dir and run that. No mas.

If you want the information to be callable anytime copy over the changed `lizzy.bat` to a folder. Add that folder to your $PATH environment variable. Now if you just hit WIN+R and type "lizzy" or "lizzy.bat" it will run.


### Changing the line

Very easy, just change the URL in the main code function to your own line and station. I've set it to Acton Main Line on the Elizabeth line. You can find the ID for your station from the TFL API website, check their UnifiedAPI resources.  

### TODO's

- [ ] Add abstraction to access codes
- [ ] Add abstraction to station and line (BIG piece of work)
- [ ] Add code to display on Raspberry Pi display
- [ ] Add code to call the function every 30 seconds
- [ ] Add a quick script to edit the lizzy.bat for the current location 