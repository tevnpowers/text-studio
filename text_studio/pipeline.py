"""Sequence of text processing components.

A text processing pipeline is a sequence of text processing components,
namely text_studio.Annotator and text_studio.Action objects that are
executed in order to produce newly annotated data and/or insights.
"""
from collections import OrderedDict

from text_studio.action import Action
from text_studio.annotator import Annotator


class Pipeline(object):
    """Sequence of text processing components.

    A text processing pipeline is a sequence of text processing components,
    namely text_studio.Annotator and text_studio.Action objects that are
    executed in order to produce newly annotated data and/or insights.

    Parameters
    -------
    id : uuid
        Unique identifier for a pipeline in a TextStudio project.
    name : string
        Display name of the pipeline in a TextStudio project.
    components : OrderedDict of text_studio.Annotator and text_studio.Action objects
        Ordered components to execute for a pipeline.

    Methods
    -------
    add_component(self, component):
        Provide new annotations for an individual data instance.
    remove_component(self, id):
        Provide new annotations for each data instance in a collection.
    execute(self, data, output_path, verbose):
        Execute the text processing pipeline on data.
    """

    def __init__(self, id, name="", components=None):
        self.id = id
        self.name = name
        self.components = components if components else OrderedDict()

    def add_component(self, component):
        """Add a new component to the end of a pipeline.

        Parameters
        ----------
        component : text_studio.Action or text_studio.Annotator
            The component to add to the pipeline.
        """
        self.components[component.id] = component

    def remove_component(self, id):
        """Remove a component from the pipeline.

        Parameters
        ----------
        id : uuid
            The id of the component to remove.
        """
        del self.components[id]

    def execute(self, data, output_path, verbose=False):
        """Execute the text processing pipeline on data.

        Parameters
        ----------
        data : collection of data instances
            Input data to be processed by the pipeline.
        output_path : string
            Location for any output from text_studio.Action objects
            in the pipeline.
        verbose : bool
            True if progress statements should be written to the console.

        Returns
        ----------
        data : collection of data instances
            The collection of input data instances, that is
            potentially modified if there are any Annotator
            components in the pipeline.
        """
        for id, component in self.components.items():
            if verbose:
                print("Executing component {}...".format(component.name))

            if isinstance(component, Annotator):
                data = component.process_batch(data)
            elif isinstance(component, Action):
                component.process_batch(data, output_path)
        return data
