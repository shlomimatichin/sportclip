#include <boost/program_options.hpp>
#include "SoundFile.h"
#include "Plot.h"

void go( const boost::program_options::variables_map & options )
{
	SoundFile input( options[ "input" ].as< std::string >().c_str() );
	Plot::Plot plot( options[ "width" ].as< unsigned >(),
			options[ "height" ].as< unsigned >() );

	plot.plot( input );
	plot.save( options[ "output" ].as< std::string >().c_str() );
}

void usage( const boost::program_options::options_description & optionsDescription )
{
	std::cout << "write me" << std::endl;
	std::cout << std::endl;
	std::cout << optionsDescription << std::endl;
}

int main( int argc, char * argv [] )
{
	boost::program_options::options_description optionsDescription( "options" );
	optionsDescription.add_options()
		("help", "produce help message")
		("input", boost::program_options::value< std::string >())
		("output", boost::program_options::value< std::string >())
		("width", boost::program_options::value< unsigned >()->default_value( 640 ))
		("height", boost::program_options::value< unsigned >()->default_value( 70 ));

	boost::program_options::variables_map options;
	try {
		boost::program_options::store(
			boost::program_options::command_line_parser( argc, argv ).
				options( optionsDescription ).run(),
			options );
		boost::program_options::notify( options );
	} catch ( boost::exception & e ) {
		TRACE_BOOST_EXCEPTION( e, "Unable to parse command line" );
		usage( optionsDescription );
		return 1;
	}

	if ( options.count( "help" ) ) {
		usage( optionsDescription );
		return 1;
	}

	try {
		go( options );
	} catch ( boost::exception & e ) {
		TRACE_BOOST_EXCEPTION( e, "Terminated on a boost exception" );
		return 1;
	} catch ( Error & e ) {
		TRACE_ERROR( "Terminated on 'Error' exception: '" << e.what() << "' at " << e.filename << ':' << e.line );
		return 1;
	} catch ( std::exception & e ) {
		TRACE_ERROR( "Terminated on std::exception: '" << e.what() );
		return 1;
	} catch ( ... ) {
		TRACE_ERROR( "Terminated on unknown exception" );
		return 1;
	}

	return 0;
}
