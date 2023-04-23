#include maps\mp\zombies\_zm_utility;
#include maps\mp\zombies\_zm_weapons;
#include maps\mp\zombies\_zm_magicbox;
// include custom;
#include scripts\zm\strings;

weapon_give_to_chat( message )
{
    if( !is_player_valid( self ) )
        return self IPrintLn( "you can only buy weapons when you are alive and playing" );

    if( !self can_buy_weapon() )
    {
        self waittill( "weapon_change_complete" );
    }

    up = isdefined_key_message( message ); // true ou false;
    alias = return_alias_message( message ); // ray gun, or m1911;
    weapon = return_struct_weapon( alias ); // weapon{ dict };

    if( isdefined( up ) && up )
    {
        return self give_weapon_upgraded( weapon );
    }

    can_buy = self can_buy_weapon_to_chat( weapon, weapon["cost"] );
    
    if( isdefined( can_buy[0] ) && can_buy[0] )
    {
        if( self HasWeapon( weapon["nameId"] ) )
        {
            self SwitchToWeapon( weapon["nameId"] );
            return self IPrintLn( "you already have this weapon" );
        }
        self.score -= weapon["cost"];
        self weapon_give( weapon["nameId"] );
    }
    else
        return self IPrintLn( can_buy[1] );
    
}

give_weapon_upgraded( weapon )
{
    if( !can_upgrade_weapon( weapon["nameId"] ) )
        return self IPrintLn( "not possible update this weapon!" );

    if( ( weapon["costUp"] + "" ) == "null" )
        return self IPrintLn( "admin disable update for this weapon!" );

    weapon_up = get_upgrade_weapon( weapon["nameId"] );
    weapon_cost = weapon["costUp"];

    if( !player_has_weapon( self GetWeaponsListPrimaries(), weapon_up ) )
    {
        can_buy = self can_buy_weapon_to_chat( weapon, weapon_cost );

        if( isdefined( can_buy[0] ) && can_buy[0] )
        {
            self.score -= weapon_cost;
            return self weapon_give( weapon_up );
        }
        else
            return self IPrintLn( can_buy[1] );
    }

    if( !can_upgrade_weapon( weapon_up ) )
        return self IPrintLn( "not possible to upgrade this weapon one more time!" );

    if( ( weapon["costReUp"] + "" )  == "null" )
        return self IPrintLn( "admin disable update for this weapon one more time! ");
    
    weapon_up = upgrade_different_weapon( self.weapon_current_up );
    weapon_cost = weapon["costReUp"];

    can_buy = self can_buy_weapon_to_chat( weapon, weapon_cost );

    if( isdefined( can_buy[0] ) && can_buy[0] )
    {
        ammo_clip = self GetWeaponAmmoClip( self.weapon_current_up );
        ammo_stock = self GetWeaponAmmoStock( self.weapon_current_up );

        if( isdefined( self.weapon_current_up ) )
            self TakeWeapon( self.weapon_current_up );

        self.score -= weapon_cost;
        self weapon_give( weapon_up );

        self SetWeaponAmmoClip( weapon_up, ammo_clip );
        self SetWeaponAmmoStock( weapon_up, ammo_stock );

        self.weapon_current_up = undefined;
    }
    else
        return self IPrintLn( can_buy[1] );
}

can_buy_weapon_to_chat( weapon, cost )
{
    if( self.score < int( cost ) )
        return array( false, "your points are insufficient to complete the purchase, points required: " + cost );

    if( level.round_number < weapon["roundUnlock"] && weapon["roundUnlock"] != "null" )
        return array( false, "weapon blocked for purchase via chat until the round: " + weapon["roundUnlock"] );

    if( self.kills < weapon["killsUnlock"] && weapon["killsUnlock"] != "null" )
        return array( false, "weapon will lock until you get the kills you need to buy it, kills: " + weapon["killsUnlock"] );

    if( self.headshots < weapon["hsUnlock"] && weapon["hsUnlock"] != "null" )
        return array( false, "weapon block until you get the necessary headshot kills: " + weapon["hsUnlock"] );

    if( weapon["limitRound"] != "null" )
    {
        if( isdefined( self.limit_buy_in_round ) && self.limit_buy_in_round == weapon["limitRound"] )
            return array( false, "the purchase limit per round for this weapon is already at the maximum: " + weapon["limitRound"] );

        self.limit_buy_in_round++;
    }

    return array( true, "can buy weapon!" );
}

player_has_weapon( weapons, weapon_buy )
{
    for( i = 0; i < weapons.size; i++ )
    {
        if( get_base_name( weapons[i] ) == get_base_name( weapon_buy ) )
        {   
            self.weapon_current_up = weapons[i];
            return true;
        }
    }
    return false;
}

upgrade_different_weapon( weapon )
{
    weapon_different = weapon;

    while( weapon_different == weapon )
    {
        weapon_different = get_upgrade_weapon( weapon, true );
    }
    
    return weapon_different;
}

is_weapon( message )
{   
    if( message.size > 3 && isdefined_key_message( message ) ) // .buy>1 ray>2 gun>3 up>4;
    {
        alias = return_alias_message( message );

        if( check_weapon_alias( alias ) )
            return true;
    }
    else if( message.size > 2 && !isdefined_key_message( message ) ) // .buy>1 ray>2 gun>3;
    {
        alias = return_alias_message( message );

        if( check_weapon_alias( alias ) )
            return true;
    }

    if( isdefined( message[1] ) ) // .buy m1911 || .buy m1911 up;
    {   
        if( check_weapon_alias( message[1] ) ) 
            return true;
    }
    return false;
}

isdefined_key_message( message )
{
    if( IsInArray( level.upgraded_Key_words, message[ message.size - 1 ] ) )
        return true;
    return false;
}

return_alias_message( message )
{
    alias = "";

    if( isdefined_key_message( message ) )
    {

        for( i = 1; i < ( message.size - 1 ); i++ )
        {
            alias += message[i] + " ";
        }

        return trim_both( alias );
    }

    for( i = 1; i < message.size; i++ )
    {
        alias += message[i] + " ";
    }

    return trim_both( alias );
}

check_weapon_alias( weapon )
{
    for( i = 0; i < level.weapons_json.size; i++ )
    {
        if( IsInArray( level.weapons_json[ level.keys_weapons[i] ]["alias"], trim_both(weapon) ) )
        {
            return true;
        }   
    }
    return false;
}

return_struct_weapon( weapon )
{
    for( i = 0; i < level.weapons_json.size; i++ )
    {
        if( IsInArray( level.weapons_json[ level.keys_weapons[i] ]["alias"], trim_both(weapon) ) )
        {
            return level.weapons_json[ level.keys_weapons[i] ];
        }   
    }
}

on_list_in_chat()
{
    level endon( "end_game" );
    
    weapon = level.weapons_json;
    keys = level.keys_weapons;
    alias = "";

    self IPrintLn( "for purchase use .buy some alias of the weapon separated by space" );
    wait 1;
    self IPrintLn( "to make a purchase with weapon upgrade put an up at the end of the command" );
    wait 1;
    self IPrintLn( "hum example of both ways exemple: .buy galil weapon no upgrade, .buy galil up upgraded weapon" );
    wait 2;
    self IPrintLn( "for improved weapons if you use the keyword at the end of the message separated from the weapon name : up, pap or pack" );
    wait 2;

    for( i = 0; i < keys.size; i++ )
    {
        for( x = 0; x < weapon[ keys[i] ]["alias"].size; x++ )
        {
            alias += x < weapon[ keys[i] ]["alias"].size - 1 ? weapon[ keys[i] ]["alias"][x] + ", " : weapon[ keys[i] ]["alias"][x];
        }
        if( weapon[keys[i]]["cost_up"] != "N/A" )
            self tell( weapon[ keys[i] ]["nameString"] + ": cost[ ^2" + weapon[ keys[i] ]["cost"] + " ^8/ ^1" + weapon[ keys[i] ]["costUp"] + " ^8] names to buy: [ " + alias + " ]" );
        else
            self tell( weapon[ keys[i] ]["nameString"] + ": cost[ ^2" + weapon[ keys[i] ]["cost"] + " ^8] names to buy: [ " + alias + " ]" ); 
        
        wait 2;

        alias = "";
    }
}