# Setting up an environment to run scripts/workflow packages
**Objective:** Try our specialized workflows when creating a large-scale collection management project

**1. (option 1) Install 'git'** to clone the repository 
* **Windows:** Download and install from [Git for Windows](https://github.com/git-guides/install-git).
* **Clone the repository** by using:
```
git clone [URL_OF_THE_REPOSITORY]
```
**2. (option 2) Download specific files** from the repository by clicking the **'Raw'** button for the file



#

### Python Scripts for Data Processing



**1. Install Python and configure [PyCharm](https://www.jetbrains.com/pycharm/download/)** *(suggested development environment, but there are many alternatives)*

* Download and install [**Python**](http://www.python.org/) -- Windows user, we recommend that you install [**Python for Windows**](https://www.python.org/downloads/windows/)

* Configure at least one [**Python interpreter**](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)

&nbsp;

**2. Install Required Libraries**

* Before running the code, ensure that you have installed the required libraries by using [**'pip'**](https://pypi.org/project/pip/)

```
pip install package-name
```
* Upgrade a package if needed
```
pip install --upgrade package-name
```
* Make a list of all installed packages
```
pip list
```
* Search for a package
```
pip search package-name
```
* Check for outdate packages
```
pip list --outdated
```
* Install packages from a requirements.txt file:
```
pip install -r requirements.txt
```
&nbsp;

**3. Using a Virtual Environment**

* Use a virtual environment for your Python projects to manage dependencies. This prevents potential conflicts between package versions across different projects.

* Install 'virtualebv'
```
pip install virtualenv
```
* Create a virtual environment
```
virtualenv myenv
```
* Activate the virtual environment *(any package you install using pip will be installed in the virtual environment, not globally)*
```
myenv\Scripts\activate
```
* Deactivate the virtual environment
```
myenv\Scripts\deactivate
```       
&nbsp;

### Testing & Documentation
**Objective:** Insights into our development - both the highs and lows.

**Usage:**

1. Acquire documentation files.
2. Adapt our lessons to your needs.
3. Test the processes.

&nbsp;

### Continuous Updates
* Stay tuned! We're always enhancing our tools and workflows.
* Don't hesitate to fork or contribute.
