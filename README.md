# *datagen*
### This project contains a number of Python files that do a variety of different tasks. These tasks are to first extract wiki-dump files into small, stripped-down html files free from links, pictures, and special characters. Then local web links are generated and appended to the html files in a hierarchal manner, several levels deep. Continuing on to the next task, the html files are sorted into a large hierarchal tree of directories with the same associated, generated links like in the first task, except with the appropriate directory path.

### The smaller tasks include generating XML files with generated links in the first task, then a task generating a random query list of words from all the html files created in the first task, and finally a task that generates JSON files containing information and specified facets for each of the html files as generated in the first task.

### While some of these tasks were tailored for performance testing and website crawling using an EC2 server on AWS with an S3 bucket to store and host the html files, this project is for anyone to use as they wish. Feel free to use and manipulate the code as desired.

*CAUTION: The links generated and appended to the html files in the first two tasks may not work on a local disk unless one manipulates the code to do so. As described above, these html files were tested with an EC2 server containing an S3 bucket in which case the links worked as intended.*

### Argument Key

`-if` or `--inputfile`

`-of` or `--outputfile`

`-id` or `--inputdir`

`-od` or `--outputdir`

*Note: If help is needed to understand what to type in a command, begin typing `python3` followed by whatever file being worked on ex. `cleanup.py` with an `-h` after it.*

*Example:*
```
python3 htmlclean.py -h
```

*Note: The instructions in this README file is more of a follow-along, feel free to copy and paste the `highlighted` examples to see what each step does. Otherwise, feel free to tweak it if necessary.*

#### Best results will happen if followed in order.

#### IMPORTANT: Before starting, please install the `tqdm` package!!!
This will show the progress bar of each individual task. Some of these tasks will take awhile so it is very useful to have! It also takes only a few seconds to install. Otherwise, feel free to take out the `import` statements containing `tqdm` at the top of each file and the word `tqdm` in the `for loops` that contain it in each file.

*Note: Assuming `pip` or `pip3` is installed, use the examples below to install `tqdm`.*

*Example1:*
```
pip install tqdm
```

### **and / or**

*Example2 (Python3):*
```
pip3 install tqdm
```


# 1. Process of Adding Links to Cleaned HTML Files

### Step 1: Downloading .bz2 Files
This instruction set will use wiki-dump files that are specifically 'dumped' articles from Wikipedia. They change every so often based on year so here is the latest link to the dump files if it changes.

*Link to Dump Files (optional):*
```
ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/20190101/
```

As an example throughout the instruction set, the links used will contain two small 11-30ish MB `.bz2` files. If there's a desire to download all the files, use the `downloadList.txt` file that contains all the links. Examples below.

*Example1:*
```
wget -P wiki_dumps ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/20190101/enwiki-20190101-pages-articles14.xml-p7697599p7744799.bz2
```
```
wget -P wiki_dumps ftp://ftpmirror.your.org/pub/wikimedia/dumps/enwiki/20190101/enwiki-20190101-pages-articles26.xml-p42567204p42663461.bz2
```

*Example2 (optional, contains all files):*
```
wget -P wiki_dumps -i downloadList.txt
```


### Step 2: Creating Both Raw HTML and Cleaned HTML Files
This step is focused on converting the downloaded `bz2` files into cleaned up `html` files.

#### First
Make sure the directory containing the `bz2` files are in the directory with all the datagen python files being used.

#### Second
Next, generate the raw (untouched) `html` files from the directory containing the `bz2` files using a slightly modified script of extraction code created by **Giuseppe Attardi** and his fellow contributors.

#### Arguments
+ First, `for file in wiki_dumps/*.bz2;` and `n=$((n+1))` mean that however many `bz2` files in the desired directory containing them, it will make sure to use all of them and organize each `bz2` file as part of a list of incrementing folders.
+ Second, `python3 htmlextract.py` means that python (specifically python 3) will run the python script `htmlextractor.py`.
+ Third, `-o ds1rawhtml/$n --html -b 25K $file` means that the output will be directed to the directory created in html format with a size of 25 KB per file.

*Example:*
```
for file in wiki_dumps/*.bz2;
do
    n=$((n+1))
    python3 htmlextract.py -o ds1rawhtml/$n --html -b 25K $file &
done
```

*Note: If running this command more than once for other purposes in the same terminal window, it will save the `n` variable and therefore will continue to increment the directory names upon the last time the command was used.*

#### Third
This will generate clean html files that will clean up unnecessary text, symbols, and links.

#### Arguments
+ First, use the directory `ds1rawhtml` containing the raw html files.
+ Second, use the directory `ds1` to put all the cleaned html files in.

*Example:*
```
python3 htmlclean.py -id ds1rawhtml -od ds1
```

*Note: This process could take quite some time depending on how many and how big the `bz2` files are.*

### Step 3: Creating a File with a List of File Paths
This step is focused on creating single text file containing multiple file paths from the ds1 directory that was recently created in the previous step.

#### Arguments
+ First, use the directory `ds1` containing the cleaned html files.
+ Second, create a new name for the text file ex. `ds1filepathlist.txt` that will contain all the file paths.

*Example:*
```
python3 htmlpathlist.py -id ds1 -of ds1filepathlist.txt
```

### Step 4: Creating a File with a List of Links Containing File Paths
This step is focused on creating single text file containing multiple links containing file paths from the ds1 directory that was created in step 2.

#### Arguments
+ First, use the directory `ds1` containing the cleaned html files.
+ Second, create a new name for the text file ex. `ds1filelinklist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmllinklist.py -id ds1 -of ds1filelinklist.txt
```

*Note: This will put all the URL links into one file*

### Step 5: Appending File Link List to Directory Containing Cleaned HTML Files
This step is focused on appending (adding) our links from `ds1filelinklist.txt` to our `ds1` directory containing the cleaned html files.

*Note: This will go in a specific order as scripted in the python3 file we are about to run. It will have a root file containing 100 links at the bottom of the file. Then the next 10 files after that will each contain 10 unique links. Then the next 100 files will each contain 10 unique links. So on an so forth.*

*Note: This will make changes to the directory containing the cleaned html files. It would be wise to make an original copy in case the links don't turn out exactly as hoped.*

Use the directory `ds1` containing the cleaned html files and then the new name of the original copy ex. `ds1_original`

*Example:*
```
cp -r ds1 ds1_original
```

#### Arguments
+ First, use the file `ds1filepathlist.txt` containing the list of file paths.
+ Second, use the file `ds1filelinklist.txt` containing the list of links with their corresponding file paths.

*Example:*
```
python3 htmlappendlink.py -if ds1filepathlist.txt -if1 ds1filelinklist.txt
```

*Note: This command may show anywhere from 1-10 progress bars. It represents how many levels deep the links will be in the `ds1`. If the last progress bar shows `0%`, it means that your `ds1` folder was less than 10 levels deep. Nothing to worry about.

### Step 6: Create Proper HTML Format For Each File
This step is focused creating proper HTML format for performance testing purposes.

#### Arguments
+ First, use the file `ds1filepathlist.txt` containing the list of file paths.

*Example*
```
python3 htmlformat.py -if ds1filepathlist.txt
```

*Note: This could take a while depending on how big and how many files being used.*

Now there should be an edited directory containing cleaned html files with links appended to them. Then a file containing a list of file paths of the cleaned html files. Finally there should also be a file containing a list of links with their associated file paths.

For testing, click on the first file inside the directory with the cleaned html files, then scroll down the 100 links added to the file. Click on the first of the 100 links and it should lead to the first file out of ten which contain 10 links each file. Keep clicking on the first link and it should have about 5-6 levels of links.


# 2. Restructuring Directory Tree with New File Paths and Links

### Step 1: Getting Rid of Subdirectories and Renaming HTML Files
This step is focused on getting rid of the subdirectories like `1, 2, 3...` and `AA`. This will also rename all the html files with a number corresponding to how many files there are.

#### First
Make sure all the files are still in the root directory or a specified directory being used from the above process of adding links to html files. They will be needed!

*Note: This is a transition phase.*

Before anything else at this point, create a temporary copy ex. `ds1tmp` of the original directory `ds1_original` created earlier.

*Example:*
```
cp -r ds1_original ds1tmp
```

#### Arguments
+ First, use the temporary directory `ds1tmp` just created.
+ Second, move the files into another temporary directory `ds4tmp` that will contain all the cleaned html files without subdirectories.

*Example:*
```
python3 htmlrestructure.py -id ds1tmp -od ds4tmp
```

Then delete the temporary directory `ds1tmp` since it's now empty.

*Example:*
```
rm -r ds1tmp
```

### Step 2: Creating a File Path List For New Temporary Directory
This step is focused on creating a new file path list for the temporary directory `ds4tmp` we just created.

#### Arguments
+ First, use the temporary directory `ds4tmp` containing the cleaned html files.
+ Second, create a new name for the temporary text file ex. `ds4tmpfilepathlist.txt` that will contain all the file paths.

*Example:*
```
python3 htmlpathlist.py -id ds4tmp -of ds4tmpfilepathlist.txt
```

### Step 3: Creating New Directory Dataset Containing Several Facet Directories
This step will create a new directory and new subdirectories that will act as file paths with facets.

#### Arguments
+ First, create a new directory ex. `ds4` that will contain all the subdirectories/facets.
+ Second, determine the number of files ex. `100000`

*Example:*
```
python3 htmlfacetdir.py -iname ds4 -inum 100000
```
### Step 4: Creating a File with a List of File Paths
This step is focused on creating single text file containing file paths from the `ds4` directory that was created earlier.

#### Arguments
+ First, use the directory `ds4` containing the cleaned html files.
+ Second, create a new name for the text file ex. `ds4filepathlist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmlfacetdirpathlist.py -iname ds4 -inum 100000 -of ds4filepathlist.txt
```

### Step 5: Copy Cleaned HTML Files to New Dataset Directory
This step will go through and copy each file in the new directory `ds4` we created to their new respective file paths.

#### Arguments
+ First, we will need the temporary text file `ds4tmpfilepathlist.txt` containing the file paths of the temporary directory `ds4tmp`
+ Second, we will need the new text file `ds4filepathlist.txt` containing the new file paths of the directory `ds4`

*Example:*
```
python3 htmlcopy.py -if ds4tmpfilepathlist.txt -if1 ds4filepathlist.txt
```

### Step 6: Creating a File with a List of Links Containing File Paths
This step is focused on creating single text file containing multiple links containing file paths from the `ds4` directory that was created earlier.

#### Arguments
+ First, use the directory `ds4` containing the cleaned html files.
+ Second, create a new name for the text file ex. `ds4filelinklist.txt` that will contain all the URL links in relation to their file paths.

*Example:*
```
python3 htmlfacetdirlinklist.py -iname ds4 -inum 100000 -of ds4filelinklist.txt
```

*Note: This will put all the URL links into one file*

### Step 7: Appending File Link List to Directory Containing Cleaned HTML Files
This step is focused on appending (adding) our links from `ds4filelinklist.txt` to our `ds4` directory containing the cleaned html files.

*Note: This will go in a specific order as scripted in the python3 file we are about to run. It will have a root file containing 100 links at the bottom of the file. Then the next 10 files after that will each contain 10 unique links. Then the next 100 files will each contain 10 unique links. So on an so forth.*

*Note: This will make changes to the directory containing the cleaned html files. It's recommended to make a copy.*

Use the directory `ds4` containing the cleaned html files and then the new name of the original copy ex. `ds4_original`

*Example:*
```
cp -r ds4 ds4_original
```

#### Arguments
+ First, use the file `ds4filepathlist.txt` containing the list of file paths.
+ Second, use the file `ds4filelinklist.txt` containing the list of links with their corresponding file paths.

*Example:*
```
python3 htmlappendlink.py -if ds4filepathlist.txt -if1 ds4filelinklist.txt
```

### Step 8: Create Proper HTML Format For Each File
This step is focused creating proper HTML format for performance testing purposes.

#### Arguments
+ First, use the file `ds4filepathlist.txt` containing the list of file paths.
+ Second, there's a way to format the html documents **without** the metadata as facets, that is, use the first example.

*Note: The first example will not use the text files `type.txt`, `file_extension.txt`, `company.txt`, `name.txt`, and `filename.txt`. These files are specifically for the second example.*

*Note: Depending on what is desired, it's best to **chose one or the other to execute**. Look at examples below to see what the results look like.*

**IMPORTANT: This first example will add the following information at the beginning and ending of each `html` file in `ds4`.**

*Note: the `<title>` information will be different per file.*

**Beginning:**
```
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<title>ds4/1/1/1/1/1/1.html</title>
</head>

<body>

...(CONTENT OF FILE)...
```

**Ending:**
```
...(CONTENT OF FILE)...
</body>
</html>
```

*Example1*
```
python3 htmlformat.py -if ds4filepathlist.txt
```

### **OR**

**IMPORTANT: This second example will add the following information at the beginning and ending of each `html` file in `ds4`.**

*Note: the `<meta>` and `<title>` information will be different per file.*

**Beginning:**
```
<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<meta name=type content="window"/>
<meta name=file_extension content=".class"/>
<meta name=company_name content="Pilgrim's Pride"/>
<meta name=created_by_name content="Yvonne Rutherford"/>
<meta name=file_name content="the_yet"/>
<title>ds4/1/1/1/1/1/1.html</title>
</head>

<body>

...(CONTENT OF FILE)...
```

**Ending:**
```
...(CONTENT OF FILE)...
</body>
</html>
```

*Example2*
```
python3 htmlformat2.py -if ds4filepathlist.txt
```

*Note: This could take a while depending on how big and how many files there are.*

There should now be a new edited directory containing cleaned html files with links appended to them. Then a file containing a list of file paths of the cleaned html files. Finally there should also be a file containing a list of links with their associated file paths.

For testing, click on the first file inside the directory with the cleaned html files, scroll down and there should be the first 100 links added to the file. Click on the on the first of the 100 links and it should direct to first file which contains 10 links to each of those files. This should continue to do this for several levels.


# 3. Creating XML Formatted Sitemaps

### Step 1: Generating Sitemaps
This step is focused on generating sitemaps in xml format and extension.

#### First
Make sure all the files are still in the root directory or a specified directory being used from the above process of adding links to html files. They will be needed!

#### Arguments
+ First, use the directory `ds1` containing the cleaned html files.
+ Second, create a new name for the `xml` file ex. `ds1sitemap.xml` that will contain all the URL links in relation to their file paths.
+ Finally, use the URL link to add to the file paths. As an example, an AWS server containing a bucket is used ex. `https://s3-us-west-2.amazonaws.com/test.bucket/`

*Example:*
```
python3 sitemaplinklist.py -id ds1 -of ds1sitemap.xml -u https://s3-us-west-2.amazonaws.com/test.bucket/
```

*Note: Make sure to put `https://` before the actual URL link!*

*Note: This will put all the URL links into one file*

### Step 2: Evenly Divide URLs Across Multiple Files
This step will sort ALL the URLs from the newly created `xml` file into multiple `xml` files with a limit of 50,000 URLs per file.

#### Arguments
+ First, create a new directory ex. `ds1sitemap` for our `xml` files to go into.
+ Second, use the `xml` file `ds1sitemap.xml` containing all the URLs.

*Example:*
```
mkdir ds1sitemap
```
```
python3 sitemapfilesplit.py -if ds1sitemap.xml
```

*Note: Don't freak out if there are a bunch of `xml` files littered in the directory. Once the process is finished, move them into the recently created directory `ds1sitemap` created for the `xml` files.*

*Example:*
```
mv sitemap*.xml ds1sitemap
```

Now there should be properly formatted `xml` files that contain URL links with their respective html file paths from the directory containing html files.


# 4. Creating a Random Generated Query List

### Step 1: Generate the Query List
This step is focused on generating a query list containing random and duplicated 1, 2, 3, and 4 token words.

#### First
Make sure all the files are still in the root directory or a specified directory being used from the above process of adding links to html files. They will be needed!

#### Arguments
+ First, use the text file `ds1filepathlist.txt` containing the list of file paths created earlier.
+ Second, create a new file ex. `ds1querylist.txt` for the query list.

*Example:*
```
python3 queryrandomlist.py -if ds1filepathlist.txt -of ds1querylist.txt
```

Now there should be a generated and randomized query list.


# 5. Creating JSON Files and a List of JSON File Paths

### Step 1: Creating JSON Files and Generating a List of JSON File Paths
This step is focused on generating a list of json files with proper formatting by adding a few facets for future testing. Also to create a list of json file paths into a single text file.

#### First
Make sure all the files are still in the root directory or a specified directory being used from the above process of adding links to html files. They will be needed!

#### Second
This will generate all the text into a single text file with proper `json` formatting.

#### Arguments
+ First, create a new directory for the `json` files to go into. One for facets as file paths ex. `ds1jsonfacetpath` and/or one for facets as data ex. `ds1jsonfacetdata` that's been collected via the text files provided.
+ Second, use the file `ds1filepathlist.txt` that contains the file paths of the directory containing all the cleaned html files.
+ Third, create a new file ex. `ds1jsonfacetpath.txt` and/or ex. `ds1jsonfacetdata.txt` as a temporary file containing all the content in `json` format.

*Example1:*
```
mkdir ds1jsonfacetpath
```

```
python3 jsontempfile.py -if ds1filepathlist.txt -of ds1jsonfacetpath.txt
```

### **and / or**

*Example2:*
```
mkdir ds1jsonfacetdata
```

```
python3 jsontempfile2.py -if ds1filepathlist.txt -of ds1jsonfacetdata.txt
```

#### Third
This will split the text into multiple files per html file with proper `json` formatting.

#### Arguments
+ First, use the temporary file `ds1jsonfacetpath.txt` and/or `ds1jsonfacetdata.txt` created earlier.

*Note: Don't freak out if there are a bunch of `json` files littered in the directory. Once the process is finished, move them into the recently created directory created for the `json` files.*

*Example1:*

**Ignore the Warning!**
```
python3 jsonfilesplit.py -if ds1jsonfacetpath.txt
```
```
find . -name "*.json" -maxdepth 1 -exec sh -c 'mv "$@" "$0"' ds1jsonfacetpath {} +
```

### **and / or**

*Example2:*

**Ignore the Warning!**
```
python3 jsonfilesplit.py -if ds1jsonfacetdata.txt
```
```
find . -name "*.json" -maxdepth 1 -exec sh -c 'mv "$@" "$0"' ds1jsonfacetdata {} +
```

*Note: This will take awhile depending on how many html files there are. The whole process could take anywhere from a few minutes to an hour.*

#### Fourth
This will generate a list of `json` file paths.

#### Arguments
+ First, use the directory `ds1jsonfacetpath` and/or `ds1jsonfacetdata` containing the json files created earlier.
+ Second, create new file ex. `ds1jsonpathlistfacetpath.txt` and/or ex. `ds1jsonpathlistfacetdata.txt` that will contain all the `json` file paths.

*Example1:*
```
python3 jsonpathlist.py -id ds1jsonfacetpath -of ds1jsonpathlistfacetpath.txt
```

### **and / or**

*Example2:*
```
python3 jsonpathlist.py -id ds1jsonfacetdata -of ds1jsonpathlistfacetdata.txt
```

Now there should be a directory containing several `json` files, each containing the correlating html file. Also a text file containing the file paths of all the `json` files that were created in the previous step.
