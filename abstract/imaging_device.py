# extended from https://gist.github.com/HazenBabcock/8d1042f564dcaee60c3a3972f2d56999


class HWPropertyValueError(Exception):
    pass


class HWProperty(object):
    """Defines a hardware property.
    """
    def __init__(self,
                 name = None,
                 value = None,
                 description = None,
                 ptype = None,
                 readable = None,
                 writable = None,
                 values = None,
                 limits = None,
                 **kwds):
        super().__init(**kwds)

        self._name = name
        self._value = value
        self._description = description
        self._ptype = ptype
        self._readable = readable
        self._writable = writable
        self._values = values
        self._limits = limits

    @property
    def name(self):
        """Name of the property.

        This is a string.
        """

    @property
    def value(self):
        """Current value of the property.

        Usually this is a string or a number but it could also be an array or any
        Python object.
        """

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise HWPropertyValueError(str(new_value) + " is not allowed.")
        
    @property
    def description(self):
        """A string that describes the property.

        This is a string describing the purpose of the property, for example
        'camera frame rate in frames per second'.
        """

    @property
    def ptype(self):
        """Type of the property (float, int, bool, str, etc..)

        This is the type of the property, for example a floating point number
        or an integer. Usually these are basic Python types, but numpy arrays
        or even 'object' are also allowed.

        FIXME: Any value in making this work with isinstance()? So for example 
               the user could use 'isinstance(hw_property, float)' and this 
               would return True of this was a floating point property? Or is 
               this just a bad idea?
        """
        
    @property
    def readable(self):
        """Is the property readable?

        This is a boolean. Do we have a use case for these kinds of properties? Do
        people use unreadable properties?
        """
        
    @property
    def writable(self):
        """Is the property writable?

        This is boolean.
        """

    @property
    def values(self):
        """Allowed values for a property.

        Usually this is a list of allowed values, or none if any value is allowed.
        """
        
    @property
    def limits(self):
        """Limits on the range of the property.

        Usually this a list [low, high], or none if there are no limits.
        """
        
    def is_valid(self, value):
        """Returns True is value is a valid setting for the property.

        This is also used internally based on the values of limits and values to
        enforce valid settings.
        """
        

class ImageData(object):
    """Contains information about one or more acquired frames. 
    """
    def __init__(self, data, meta):
        self._data = data
        self._meta = meta

    @property
    def data(self):
        """Image data array for this frame.

        Usually a numpy array, but may also be another array-like data type to support cameras that
        stream to disk.

        If the image data is unavailable (for example, because it has been overwritten already),
        raise an exception.
        """

    @property
    def is_transient(self):
        """Bool indicating whether this image data is stored in a transient buffer and may be overwritten
        in the future.
        """

    @property
    def meta(self):
        """Dictionary of metadata describing image acquisition, containing:

        camera_properties : dict
            Contains {property:value} pairs that were used in the acquisition of this frame data
        data_axes : tuple
            Describes data array axes; may contain: ('frame', 'row', 'col', 'channel')
        format : str
            Describes the image data format (For example: 8-, 12-, 16- bit integer packing? Uncommon colorspaces?)
        timestamp : float
            CPU clock time at which frame arrived in software

        Note: parts of this stucture may be shared between ImageData instances (particularly camera_properties)
        """


class ImagingDevice(object):

    @classmethod
    def list_devices(cls):
        """Return a list of available [device_id] objects that can be used to construct
        an ImagingDevice instance.

        Returns an empty list if no devices are found; raises an exception if unable to
        check (if this ImagingDevice subclass is not supported for some reason).
        """

    def __init__(self, device_id):
        """Create and open an imaging device.

        Parameters
        ----------
        camera_id : object
            Uniquely identifies the camera to open. The type of this object is defined by the 
            ImagingDevice subclass.
        """
        self.properties_used = {}

    def open():
        # open camera

    def close():
        # Shutdown / clean up.
        
    def get_properties(self, property_names):
        """Return a dictionary of {'property_name': HWProperty} for the list of properties requested.
        """
        for elt in property_names:
            prop = .. # Create property with current value.
            p_dict[elt] = prop

            # Add to record of properties of interest.
            if not elt in self.properties_used:
                self.properties_used[elt] = prop

        return p_dict
        
    def get_property_info(self):
        """Return information about all properties supported by this device

        Return format is::

            { 'property_name': HWProperty }

        Some property names are standardized across all cameras (although cameras need not
        support all of these):

            acquire_mode : 'free_run' | 'fixed_length'
            fixed_frame_count : int
            trigger_mode : 
                'none' : start immediately on start_acquisition()
                'trigger_first' : wait for trigger before starting first frame
                'trigger_frames' : wait for trigger before starting each frame
                'trigger_exposure' : expose only when trigger is high
            protect_data : bool
                If the ImagingDevice subclass normally produces ImageData.is_transient==True, then
                this forces image data to be copied to prevent possible frame loss.
            buffer_size : int
                If the ImagingDevice subclass uses a fixed-size buffer to acquire image data, this
                property determines the buffer size in frames.
            bit_depth : int
                Bits per pixel to acquire
            exposure_time : float
            frame_rate : float
            binning_x : int
            binning_y : int
            region_x : int    # region properties are expressed relative to the _unbinned_ sensor pixels
            region_y : int
            region_width : int
            region_height : int
            sensor_width : int
            sensor_height : int
            pixel_width : float
            pixel_height : float
            camera_model : str

        Any extra property names are determined by the camera driver.

        """
        # Returns information about a property (type, range, if it exists).
        
    def set_properties(self, properties):
        """Set the value of device properties.

        Parameters
        ----------
        properties : dict or list
            dict: Contains {'property_name': value} pairs to be set. May be OrderedDict in cases where
            properties must be set in a specific order.
            list: A list of HWProperty objects.

        Returns
        -------
        need_restart : bool
            Indicates whether acquisition must be restarted before new values take effect
        new_values : dict
            Contains {'property_name': HWProperty} for each property that was set. In some cases,
            the value returned here will differ from the one requested. May also contain
            the values of properties that were indirectly changed as a result of this
            request.
        info_changed : list
            A list of properties that may have changed results from get_property_info as
            a result of this request. This allows user interfaces to update dynamically as needed.
        """
        new_values = {}
        for elt in properties:
            if isinstance(elt, HWProperty):
                # update based on elt.value
            else:
                # update based on properties[elt]

            # Query updated value.
            prop = .. # Create property with current value.
            new_values[elt] = prop

            # Add to record of properties that the user specifically requested.
            #
            # FIXME? Need to do something here so that this property also gets picked up
            #        as changed?
            if not elt in self.properties_used:
                self.properties_used[elt] = prop

        # Check for changes in the properties that the user is tracking.
        #
        # FIXME? Some properties are going to be queried multiple times which may not
        #        be efficient. Perhaps 'new_values' and 'info_changed' are mutually
        #        exclusive?
        #
        changed = {}
        for elt in self.properties_used:
            prop = .. # Create property with current value.
            if (prop.value != self.properties_used[elt].value):
                changed[elt] = prop
    
    def get_images(self, max_count=None):
        """Return ImageData instances that have accumulated since the last call to get_images().

        Parameters
        ----------
        max_count : int | None
            If specified, then only the *max_count* most recent images are returned; 
            older frames are discarded (this allows avoiding the overhead of creating
            ImageData instances that will not be used).
        """

    def start_acquisition(self):
        """Start image acquisition.
        """
        
    def is_acquiring(self):
        """Return bool indicating whether the camera is currently acquiring frames.

        If False, then it is guaranteed no more frames will arrive from the device.
        """

    def stop_acquisition(self):
        """Stop image acquisition.

        Note: after calling this method, it is possible that is_acquiring will still be True
        and frames may continue to arrive from the camera for some time.
        """

    def set_callback(self, callback):
        """Set a callback to be invoked on camera events such as the arrival of a new frame or 
        when acquisition has stopped.

        Callback parameters
        -------------------
        event_type : str
            "frame", "stop", "error"
        event_info : object
            Extra information about the event

        Note: the callback is invoked from a background thread, so it must be thread-safe
        """




# Usage examples.

cam = ImagingDevice(device_id="XYZZY")
result = cam.set_properties({
    'region_width': 512,
    'region_height': 512,
    'frame_rate': 10.0,
    'acquire_mode': 'fixed_length',
    'fixed_frame_count': 10,
})

cam.start_acquisition()
while cam.is_acquiring():
    time.sleep(0.1)
images = cam.get_images()  # len(images) = 10


cam.set_properties({
    'acquire_mode': 'free_run'.
    'protect_data': True,
})

cam.start_acquisition()
time.sleep(2.0)
cam.stop_acquisition()

images = cam.get_images()  # len(images) ~= 20
images[0].data  # guaranteed to succeed since protect_data==True


cam.set_properties({
    'protect_data': False,
})

cam.start_acquisition()
time.sleep(2.0)
cam.stop_acquisition()

images = cam.get_images()  # len(images) ~= 20
images[0].data  # raises exception if data has already been overwritten
