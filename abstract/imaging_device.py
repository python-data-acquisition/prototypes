
class ImagingDeviceException(Exception):
  pass
  
class ImagingDevice(object):

  def __init__(self, ..):
    # Initialize the imaging device
    
  def close():
    # Shutdown / clean up.
    
  def getProperty(self, p_name):
    # Returns the current value of a property of the device.
    
  def getPropertyInfo(self, p_name):
    # Returns information about a property (type, range, if it exists).
    
  def setProperty(self, p_name, p_value):
    # Sets the value of a property of the device.
    
  def getImages(self):
    # Return all images currently in the buffer.
    
  def startAcquisition(self):
    # Start acquiring images.
    
  def stopAcquisition(self):
    # Stop acquiring image.
    
# Usage examples.

cam = ImagingDevice(camera_id = "XYZZY")
cam.setProperty("width", 512)
cam.setProperty("height", 512)
cam.setProperty("fps", 10.0)
cam.setProperty("acquisition_mode", "fixed_length")
cam.setProperty("number_frames", 10)

cam.startAcquisition()
time.sleep(2.0)
cam.stopAcquisition()

images = cam.getImages() # len(images) = 10

cam.setProperty("run_till_abort")

cam.startAcquisition()
time.sleep(2.0)
cam.stopAcquisition()

images = cam.getImages() # len(images) = 20