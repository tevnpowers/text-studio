# TextStudio
*TextStudio* is a text processing architecture comprised of the `text-studio` Python package, software development kit (SDK), and desktop application. Each of these components contributes to creating the development environment where users can explore, process, model, and visualize textual data.

The following documentation pertais specifically to `text-studio`, the Python package which supports the software development kit (SDK).

## Installation
`pip install text-studio`

OR

`git clone https://github.com/tevnpowers/text-studio`

## Data Loader
A Data Loader is responsible for loading data that exists outside of the application into a canonical *TextStudio* data set. It must also provide the inverse functionality, to write a *TextStudio* data set to an external location.

A `DataLoader` plugin is a subclass of the `text_studio.DataLoader` abstract class, and implements the following class methods:

 - `load`: Create the list of data instances for a `text_studio.Dataset`from data that exists outside of the application.
     - Parameters:
         - `file_path`: The path to a data file or directory which contains data files to be loaded into a data set.
         - `**kwargs`: Additional keyword arguments that the author can optionally require in order to configure the load logic.
     - Return:
         - List of dictionary objects, each of which represents a single data instance in the data set.
 - `save`: Export the list of data instances in a `text_studio.Dataset` to a storage system outside of the application.
     - Parameters:
          - `file_path`: The path to a data file or directory where the data set should be exported.
         - `**kwargs`: Additional keyword arguments that the author can optionally require in order to configure the save logic.
     - Return:
         - Boolean value that is `True` if a data set is successfully exported and `False` if the save failed for any reason.

## Pipeline
A text processing pipeline is any combination of Annotator or Action components that run in a sequence on an input data set. Pipelines themselves are implemented by `text_studio.Pipeline`. In general, Pipelines will be instantiated by the *TextStudio* desktop application, not by developers.

However, developers may write plugins for each pipeline component type further described below.

### Annotator
An Annotator runs a process which augments the input data it is given. That is, given a data instance object (Python dictionary), an annotator will add a new key value pair to the dictionary (e.g. tokenization output, part of speech tags, lemmatized version of the raw text, etc.).

An `Annotator` plugin is a subclass of the `text_studio.Annotator` abstract class, and implements the following class methods:
- `__init__`: Configure the settings needed for the Annotator module to properly function. 
    - Parameters:
        - `keys`: the list of keys (strings) in the data instance object dictionary correspond to the values that the Annotator needs in order to extract the data required for execution.
        - `annotations`: the list of keys (strings) that an Annotator should add to the data instance object dictionary, where the corresponding value(s) are computed by the Annotator when executed.
        - Additional Named Arguments: A plugin author may require any arbitrary named arguments that are necessary to configure the module's execution.
- `process_single`: Annotate a single data instance with a new value.
    - Parameters:
        - `doc`: A dictionary representing a single data instance. 
    - Return:
        - A dictionary that is the augmented version of the input object, now annotated with additional information.
- `process_batch`: Annotate a collection of data instances with new values.
    - Parameters:
        - `docs`: An iterable containing dictionaries, which each represent a single data instance.
    - Return:
        - A collection of dictionaries, where each is an augmented version of an input object, now annotated with additional information.

### Action
An Action consumes input data either individually or in bulk in order to produce an artifact about the input data, while not modifying or augmenting the input data instance(s). In this case, an artifact may be a visualization, a summary report, or any other insights that can be extracted from the provided data.

An `Action` plugin is a subclass of the `text_studio.Action` abstract class, and implements the following class methods:
- `__init__`: Configure the settings needed for the Action module to properly function. 
    - Parameters:
        - `keys`: the list of keys (strings) in the data instance object dictionary correspond to the values that the Action needs in order to extract the data required for execution.
        - Additional Named Arguments: A plugin author may require any arbitrary named arguments that are necessary to configure the module's execution.
- `process_single`: Process a single data instance to produce insights.
    - Parameters:
        - `doc`: A dictionary representing a single data instance. 
information.
- `process_batch`: Process a collection of data instances to produce insights.
    - Parameters:
        - `docs`: An iterable containing dictionaries, which each represent a single data instance.