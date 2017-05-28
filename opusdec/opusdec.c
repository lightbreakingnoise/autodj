#include <Python.h>
#include <stdlib.h>
#include <opus/opus.h>

OpusDecoder *dec;

PyObject *initialize(PyObject *self, PyObject *args) {
	int i;

	dec = opus_decoder_create( 48000, 2, &i );

	PyObject *result;
	result = Py_BuildValue("i", 0);
	return result;
}

PyObject *decode(PyObject *self, PyObject *args) {
	const char *raw;
	int len;
	
	if( !PyArg_ParseTuple(args, "y#", &raw, &len) )
		return NULL;
	
	short pcm[960];
	unsigned char *input;
	input = (unsigned char*)raw;
	
	int rc;
	rc = opus_decode( dec, input, len, pcm, 480, 0 );
	
	rc += 1;
	
	PyObject *result;
	result = Py_BuildValue("y#", (char*)pcm, 1920);
	return result;
}

static PyMethodDef module_methods[] = {
	{ "initialize", initialize, METH_NOARGS, NULL },
	{ "decode", decode, METH_VARARGS, NULL },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef opusdecmodules = {
	PyModuleDef_HEAD_INIT,
	"opusdec",
	NULL,
	-1,
	module_methods
};

PyMODINIT_FUNC PyInit_opusdec(void) {
	return PyModule_Create( &opusdecmodules );
}
