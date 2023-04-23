trim_both( string )
{
    return trim_end( trim_start( string ) );
}
 
trim_start( string )
{
    if( string.size < 1 )
        return printf( "string vazio!" );

    if( string[0] == " " )
    {
        string_ = "";

        for( i = 0; i < string.size; i++ )
        {
            if( string[i] != " " )
            {
                for( x = i; x < string.size; x++ )
                {
                    string_ += string[x];
                }
                return string_.size > 0 ? string_: printf( "string space!" );
            }
        }
    }
    return string;
}

trim_end( string )
{
    if( string.size < 1 )
        return printf( "string vazio!" );

    if( string[string.size - 1] == " " )
    {
        string_ = "";

        for( i = string.size - 1; i > -1; i-- )
        {
            if( string[i] != " " )
            {
                for( x = 0; x < (i + 1); x++ )
                {
                    string_ += string[x];
                }
                return string_.size > 0 ? string_: printf( "string space!" );
            }
        }
    }
    return string;
}