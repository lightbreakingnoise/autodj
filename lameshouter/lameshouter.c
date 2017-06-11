#include <Python.h>
#include <stdlib.h>
#include <lame/lame.h>
#include <shout/shout.h>

lame_global_flags *gfp;
shout_t *shout;

PyObject *init(PyObject *self, PyObject *args) {
	gfp = lame_init();
	lame_set_num_channels( gfp, 2 );
	lame_set_in_samplerate( gfp, 48000 );
	lame_set_VBR( gfp, 1 );
	lame_set_mode( gfp, 1 );
	lame_set_quality( gfp, 2 );
	lame_init_params( gfp );

	shout = shout_new();
	shout_set_host( shout, "127.0.0.1" );
	shout_set_protocol( shout, SHOUT_PROTOCOL_HTTP );
	shout_set_port( shout, 8000 );
	shout_set_password( shout, "hackme" );
	shout_set_mount( shout, "/radio.mp3" );
	shout_set_user( shout, "source" );
	shout_set_format( shout, SHOUT_FORMAT_MP3 );
	shout_open( shout );

	PyObject *result;
	result = Py_BuildValue("");
	return result;
}

PyObject *shouter(PyObject *self, PyObject *args) {
	const char *raw;
	int len;
	
	if( !PyArg_ParseTuple(args, "y#", &raw, &len) )
		return NULL;

	if( len != 8192 )
		return NULL;

	unsigned char mp3[4096];
	short *pcm;
	pcm = (short*)raw;

	int rc;

	rc = lame_encode_buffer_interleaved( gfp, pcm, 2048, mp3, 4096 );
	if( rc > 0 )
		shout_send( shout, mp3, rc );

	PyObject *result;
	result = Py_BuildValue("");
	return result;
}

PyObject *setmeta(PyObject *self, PyObject *args) {
	const char *dta;

	if( !PyArg_ParseTuple(args, "s", &dta) )
		return NULL;
	
	shout_metadata_t *m;
	m = shout_metadata_new();
	shout_metadata_add(m, "song", dta);
	shout_set_metadata(shout, m);
	shout_metadata_free(m);
	
	PyObject *result;
	result = Py_BuildValue("");
	return result;
}

static PyMethodDef module_methods[] = {
	{ "init", init, METH_NOARGS, NULL },
	{ "shouter", shouter, METH_VARARGS, NULL },
	{ "setmeta", setmeta, METH_VARARGS, NULL },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef modules = {
	PyModuleDef_HEAD_INIT,
	"lameshouter",
	NULL,
	-1,
	module_methods
};

PyMODINIT_FUNC PyInit_lameshouter(void) {
	return PyModule_Create( &modules );
}
