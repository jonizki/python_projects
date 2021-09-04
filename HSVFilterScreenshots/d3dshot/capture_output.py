import enum


class CaptureOutputs(enum.Enum):
    PIL = 0
    NUMPY = 1
    NUMPY_FLOAT = 2


class CaptureOutputError(BaseException):
    pass


class CaptureOutput:
    def __init__(self, backend=CaptureOutputs.PIL):
        self.backend = self._initialize_backend(backend)

    def process(self, pointer, pitch, size, width, height, region, rotation):
        return self.backend.process(pointer, pitch, size, width, height, region, rotation)

    def to_pil(self, frame):
        return self.backend.to_pil(frame)

    def stack(self, frames, stack_dimension):
        return self.backend.stack(frames, stack_dimension)

    def _initialize_backend(self, backend):
        if backend == CaptureOutputs.PIL:
            from d3dshot.capture_outputs.pil_capture_output import PILCaptureOutput

            return PILCaptureOutput()
        elif backend == CaptureOutputs.NUMPY:
            from d3dshot.capture_outputs.numpy_capture_output import NumpyCaptureOutput

            return NumpyCaptureOutput()
        elif backend == CaptureOutputs.NUMPY_FLOAT:
            from d3dshot.capture_outputs.numpy_float_capture_output import NumpyFloatCaptureOutput
 
        else:
            raise CaptureOutputError("The specified backend is invalid!")
