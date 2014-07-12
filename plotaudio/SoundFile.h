#ifndef __SOUND_FILE_H__
#define __SOUND_FILE_H__

#include <sndfile.h>
#include "Debug.h"
#include "Error.h"

class SoundFile
{
public:
	SoundFile( const char * filename ) :
		_file( nullptr )
	{
		_file = sf_open( filename, SFM_READ, & _info );
		if ( _file == nullptr ) {
			sf_close( _file );
			THROW( Error, "Unable to open file " << filename << " as audio" );
		}
		if ( ( _info.format & SF_FORMAT_SUBMASK ) != SF_FORMAT_PCM_16 ) {
			sf_close( _file );
			THROW( Error, "Only 16 bit audio is currently supported" );
		}
		if ( channels() > 2 ) {
			sf_close( _file );
			THROW( Error, "Only mono and stereo audio is currently supported" );
		}
	}

	~SoundFile()
	{
		sf_close( _file );
	}

	const SF_INFO & info() const { return _info; }
	size_t frames() const { return _info.frames; }
	int samplerate() const { return _info.samplerate; }
	int channels() const { return _info.channels; }

	short nextMonoSample()
	{
		short raw[2];
		sf_count_t count = sf_readf_short(_file, raw, 1);
		if ( count != 1 )
			THROW( Error, "Error reading samples. EOF?" );
		if ( channels() == 2 )
			return static_cast< short >(
				( static_cast< int >( raw[ 0 ] ) + raw[ 1 ] ) / 2 );
		else
			return raw[ 0 ];
	}

	std::vector< short > allMono()
	{
		std::vector< short > out( frames() * channels() );
		sf_count_t count = sf_readf_short(_file, & out[ 0 ], frames() );
		if ( count != static_cast< sf_count_t >( frames() ) )
			THROW( Error, "Error reading samples" );
		if ( channels() == 2 ) {
			for ( unsigned i = 0; i < frames(); ++ i )
				out[ i ] = ( out[ i * 2 ] + out[ i * 2 + 1 ] ) / 2;
			out.resize( out.size() / 2 );
		}
		return std::move( out );
	}

private:
	SNDFILE *  _file;
	SF_INFO    _info;

	SoundFile( const SoundFile & rhs ) = delete;
	SoundFile & operator= ( const SoundFile & rhs ) = delete;
};


#endif // __SOUND_FILE_H__
