#include maps\mp\zombies\_zm_weapons;
// include custom;
#include scripts\zm\strings;
#include scripts\zm\func_weapons;

init()
{   
    level.upgraded_Key_words = [];
    level.upgraded_Key_words[level.upgraded_Key_words.size] = "up";
    level.upgraded_Key_words[level.upgraded_Key_words.size] = "pap";
    level.upgraded_Key_words[level.upgraded_Key_words.size] = "pack";

    thread has_file_weapons();
    thread message_buy_weapon();
    thread upgraded_list_weapons();
}

upgraded_list_weapons()
{
    SetDvar( "wp_list", "none" );
    for(;;)
    {
        dvar = getDvar( "wp_list" );

        if( dvar != "none" )
        {
            switch ( dvar ) 
            {
                case "up":
                case "on":
                    has_file_weapons();
                    break;

                case "list":
                    thread list_weapons();
                    break;

                default:
                    printf( "command invalid! \n commands: \"up\", \"on\" or \"list\"" );
            }
            setDvar( "wp_list", "none" );
        }
        wait 1;
    }
}

check_file_weapons_exists()
{
    return fileExists( "scripts/zm/weapons_list.json" );
}

has_file_weapons()
{
    if( isdefined( level.loading_weapons_json ) && level.loading_weapons_json )
        return printf( "your request is already being processed... \n checks if the weapons file exists!" );

    level.loading_weapons_json = true;

    for(;;)
    {
        if( check_file_weapons_exists() )
        {
            thread open_file_weapons();

            level.loading_weapons_json = false;

            return;
        }
        wait 0.5;
    }
}

open_file_weapons()
{   
    level.weapons_json = current_map_weapons( jsonParse( readFile( "scripts/zm/weapons_list.json" ) ) );
    return printf( "file to weapons online!" );   
}

current_map_weapons( weapons_list )
{
    keys = GetArrayKeys( weapons_list );
    weapons = [];   

    level.keys_weapons = [];
    
    for( i = 0; i < keys.size; i++ )
    {
        if( !is_weapon_included( keys[i] ) )
            continue;

        weapons[keys[i]] = weapons_list[ keys[i] ];

        level.keys_weapons[level.keys_weapons.size] = keys[i];
    }
    return weapons;
}

list_weapons()
{
    if( !isdefined( level.weapons_json ) )
        return printf( "you have not loaded the weapons file yet. command: \"wp_list on\"" );

    for( i = 0; i < level.weapons_json.size; i++ )
    {   
        printf( level.weapons_json[ level.keys_weapons[i] ]["nameString"] );
        wait 0.5;
    }
}

message_buy_weapon()
{
    level endon( "end_game" );

    for(;;)
    {
        level waittill( "say", message, player );

        message =  StrTok( trim_both( message ), " " );

        if( isdefined( message[0] ) && message[0] == ".buy" )
        {
            if( is_weapon( message ) )
            {
                player weapon_give_to_chat( message );
                continue;
            }
            player IPrintLn( "weapon does not exist try to use the command to check the weapons: .list" );
        }
        else if( isdefined( message[0] ) && message[0] == ".list" )
            player thread on_list_in_chat();
    }
}

