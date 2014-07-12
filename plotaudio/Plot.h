#ifndef __PLOT_H__
#define __PLOT_H__

#include <Magick++.h>

namespace Plot
{

using namespace Magick;

class Plot
{
public:
	Plot(unsigned width, unsigned height ):
		_width( width ),
		_height( height ),
		_image( Geometry( width, height ),
			Color( 0, 0, 0, QuantumRange ) )
	{}

	void plot( SoundFile & soundFile )
	{
		Color blue( 0, 0, QuantumRange * 3 / 5, 0 );
		std::vector< short > allMono = soundFile.allMono();
		std::vector< int > top( _width );
		std::vector< int > bottom( _width );
		for ( unsigned i = 0; i < _width; ++ i ) {
			top[ i ] = _height / 2;
			bottom[ i ] = _height / 2;
		}
		for ( unsigned i = 0; i < allMono.size(); ++ i ) {
			int x = static_cast< long long >( i ) * _width / allMono.size();
			int y = _height / 2 + allMono[ i ] * ( (int)(_height) / 2 ) / ( 1 << 15 );
			if ( top[ x ] > y )
				top[ x ] = y;
			if ( bottom[ x ] < y )
				bottom[ x ] = y;
		}
		for ( unsigned x = 0; x < _width; ++ x )
			for ( int y = top[ x ]; y <= bottom[ x ]; ++ y )
				_image.pixelColor( x, y, blue );
	}

	void save( const char * filename )
	{
		_image.write( filename );
	}

private:
	unsigned       _width;
	unsigned       _height;
	Magick::Image  _image;

	Plot( const Plot & rhs ) = delete;
	Plot & operator= ( const Plot & rhs ) = delete;
};

}

#endif // __PLOT_H__
