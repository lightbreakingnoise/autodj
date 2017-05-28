#include <Python.h>
#include <stdlib.h>
#include <opus/opus.h>

OpusEncoder *enc;

PyObject *initialize(PyObject *self, PyObject *args) {
	int bitrate;
	
	if( !PyArg_ParseTuple(args, "i", &bitrate) )
		return NULL;
	
	int i;

	enc = opus_encoder_create( 48000, 2, OPUS_APPLICATION_VOIP, &i );
	opus_encoder_ctl( enc, OPUS_SET_BITRATE(bitrate) );
	opus_encoder_ctl( enc, OPUS_SET_COMPLEXITY(10) );
	opus_encoder_ctl( enc, OPUS_SET_SIGNAL(OPUS_SIGNAL_MUSIC) );

	PyObject *result;
	result = Py_BuildValue("i", bitrate);
	return result;
}

PyObject *encode(PyObject *self, PyObject *args) {
	const char *raw;
	int len;
	
	if( !PyArg_ParseTuple(args, "y#", &raw, &len) )
		return NULL;
	
	short *pcm;
	pcm = (short*)raw;
	unsigned char *output;
	output = (unsigned char*) malloc( 500 );
	
	int rc;
	rc = opus_encode( enc, pcm, 480, output, 500 );
	
	PyObject *result;
	result = Py_BuildValue("y#", (char*)output, rc);
	return result;
}

static PyMethodDef module_methods[] = {
	{ "initialize", initialize, METH_VARARGS, NULL },
	{ "encode", encode, METH_VARARGS, NULL },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef opusencmodules = {
	PyModuleDef_HEAD_INIT,
	"opusenc",
	NULL,
	-1,
	module_methods
};

PyMODINIT_FUNC PyInit_opusenc(void) {
	return PyModule_Create( &opusencmodules );
}
