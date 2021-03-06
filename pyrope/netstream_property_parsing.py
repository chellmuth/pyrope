from pyrope.utils import reverse_bytewise, BOOL, read_serialized_vector, read_float_vector
from pyrope.exceptions import PropertyParsingError
# God damn I wish python had fall through like any normal switch-case syntax <.<
# But you know, explicit is better than implicit...yeah, fuck you
# thanks to https://github.com/jjbott/RocketLeagueReplayParser/
# he has done a shitton of work on this
parsing = {
    # FLAGGED INT Properties (At least i assume its a flag + 32 bit int)
    "TAGame.Team_TA:GameEvent": lambda x: _read_flagged_int(x),
    "TAGame.CrowdActor_TA:ReplicatedOneShotSound": lambda x: _read_flagged_int(x),
    "TAGame.CrowdManager_TA:ReplicatedGlobalOneShotSound": lambda x: _read_flagged_int(x),
    "Engine.Actor:Owner": lambda x: _read_flagged_int(x),
    "Engine.GameReplicationInfo:GameClass": lambda x: _read_flagged_int(x),
    "Engine.PlayerReplicationInfo:Team": lambda x: _read_flagged_int(x),
    "TAGame.CrowdManager_TA:GameEvent": lambda x: _read_flagged_int(x),
    "Engine.Pawn:PlayerReplicationInfo": lambda x: _read_flagged_int(x),
    "TAGame.PRI_TA:ReplicatedGameEvent": lambda x: _read_flagged_int(x),
    "TAGame.Ball_TA:GameEvent": lambda x: _read_flagged_int(x),
    "Engine.Actor:ReplicatedCollisionType": lambda x: _read_flagged_int(x),
    "TAGame.CrowdActor_TA:GameEvent": lambda x: _read_flagged_int(x),
    "TAGame.Team_TA:LogoData": lambda x: _read_flagged_int(x),
    "TAGame.CarComponent_TA:Vehicle": lambda x: _read_flagged_int(x),

    # INT properties, seems to make sense
    "TAGame.GameEvent_Soccar_TA:SecondsRemaining": lambda x: _read_int(x),
    "TAGame.GameEvent_TA:ReplicatedGameStateTimeRemaining": lambda x: _read_int(x),
    "TAGame.CrowdActor_TA:ReplicatedCountDownNumber": lambda x: _read_int(x),
    "TAGame.GameEvent_Team_TA:MaxTeamSize": lambda x: _read_int(x),
    "Engine.PlayerReplicationInfo:PlayerID": lambda x: _read_int(x),
    "TAGame.PRI_TA:TotalXP": lambda x: _read_int(x),
    "TAGame.PRI_TA:MatchScore": lambda x: _read_int(x),
    "TAGame.GameEvent_Soccar_TA:RoundNum": lambda x: _read_int(x),
    "TAGame.GameEvent_TA:BotSkill": lambda x: _read_int(x),
    "TAGame.PRI_TA:MatchShots": lambda x: _read_int(x),
    "TAGame.PRI_TA:MatchSaves": lambda x: _read_int(x),
    "ProjectX.GRI_X:ReplicatedGamePlaylist": lambda x: _read_int(x),
    "Engine.TeamInfo:Score": lambda x: _read_int(x),
    "Engine.PlayerReplicationInfo:Score": lambda x: _read_int(x),
    "TAGame.PRI_TA:MatchGoals": lambda x: _read_int(x),
    "TAGame.PRI_TA:MatchAssists": lambda x: _read_int(x),
    "ProjectX.GRI_X:ReplicatedGameMutatorIndex": lambda x: _read_int(x),
    "TAGame.PRI_TA:Title": lambda x: _read_int(x),

    # BYTE Properties
    "Engine.PlayerReplicationInfo:Ping": lambda x: _read_byte(x),
    "TAGame.Vehicle_TA:ReplicatedSteer": lambda x: _read_byte(x),
    "TAGame.Vehicle_TA:ReplicatedThrottle": lambda x: _read_byte(x),
    "TAGame.PRI_TA:CameraYaw": lambda x: _read_byte(x),
    "TAGame.PRI_TA:CameraPitch": lambda x: _read_byte(x),
    "TAGame.Ball_TA:HitTeamNum": lambda x: _read_byte(x),
    "TAGame.GameEvent_Soccar_TA:ReplicatedScoredOnTeam": lambda x: _read_byte(x),
    "TAGame.GameEvent_TA:ReplicatedStateIndex": lambda x: _read_byte(x),  # maybe?
    "TAGame.CarComponent_TA:ReplicatedActive": lambda x: _read_byte(x),

    # BOOLEAN Properties
    "Engine.Actor:bCollideWorld": lambda x: _read_bool(x),
    "Engine.PlayerReplicationInfo:bReadyToPlay": lambda x: _read_bool(x),
    "TAGame.Vehicle_TA:bReplicatedHandbrake": lambda x: _read_bool(x),
    "TAGame.Vehicle_TA:bDriving": lambda x: _read_bool(x),
    "Engine.Actor:bNetOwner": lambda x: _read_bool(x),
    "Engine.Actor:bBlockActors": lambda x: _read_bool(x),
    "TAGame.GameEvent_TA:bHasLeaveMatchPenalty": lambda x: _read_bool(x),
    "TAGame.PRI_TA:bUsingBehindView": lambda x: _read_bool(x),
    "TAGame.PRI_TA:bUsingSecondaryCamera": lambda x: _read_bool(x),
    "TAGame.GameEvent_TA:ActivatorCar": lambda x: _read_bool(x),
    "TAGame.GameEvent_Soccar_TA:bOverTime": lambda x: _read_bool(x),
    "ProjectX.GRI_X:bGameStarted": lambda x: _read_bool(x),
    "Engine.Actor:bCollideActors": lambda x: _read_bool(x),
    "TAGame.PRI_TA:bReady": lambda x: _read_bool(x),
    "TAGame.RBActor_TA:bFrozen": lambda x: _read_bool(x),
    "Engine.Actor:bHidden": lambda x: _read_bool(x),
    "Engine.Actor:bTearOff": lambda x: _read_bool(x),
    "TAGame.CarComponent_FlipCar_TA:bFlipRight": lambda x: _read_bool(x),
    "Engine.PlayerReplicationInfo:bBot": lambda x: _read_bool(x),
    "Engine.PlayerReplicationInfo:bWaitingPlayer": lambda x: _read_bool(x),
    "TAGame.RBActor_TA:bReplayActor": lambda x: _read_bool(x),
    "TAGame.PRI_TA:bIsInSplitScreen": lambda x: _read_bool(x),
    "Engine.GameReplicationInfo:bMatchIsOver": lambda x: _read_bool(x),
    "TAGame.CarComponent_Boost_TA:bUnlimitedBoost": lambda x: _read_bool(x),

    # FLOAT Properties
    "TAGame.CarComponent_FlipCar_TA:FlipCarTime": lambda x: _read_float(x),
    "TAGame.Ball_TA:ReplicatedBallScale": lambda x: _read_float(x),
    "TAGame.CarComponent_Boost_TA:RechargeDelay": lambda x: _read_float(x),
    "TAGame.CarComponent_Boost_TA:RechargeRate": lambda x: _read_float(x),
    "TAGame.Ball_TA:ReplicatedAddedCarBounceScale": lambda x: _read_float(x),
    "TAGame.Ball_TA:ReplicatedBallMaxLinearSpeedScale": lambda x: _read_float(x),
    "TAGame.Ball_TA:ReplicatedWorldBounceScale": lambda x: _read_float(x),
    "TAGame.CarComponent_Boost_TA:BoostModifier": lambda x: _read_float(x),
    "Engine.Actor:DrawScale": lambda x: _read_float(x),
    "TAGame.CrowdActor_TA:ModifiedNoise": lambda x: _read_float(x),

    # STRING Properties
    "Engine.GameReplicationInfo:ServerName": lambda x: _read_string(x),
    "Engine.PlayerReplicationInfo:PlayerName": lambda x: _read_string(x),
    "TAGame.Team_TA:CustomTeamName": lambda x: _read_string(x),

    # S.P.E.C.I.A.L
    "TAGame.RBActor_TA:ReplicatedRBState": lambda x: _read_rigid_body_state(x),
    "Engine.PlayerReplicationInfo:UniqueId": lambda x: _read_unique_id(x),
    "TAGame.PRI_TA:PartyLeader": lambda x: _read_unique_id(x),
    "TAGame.PRI_TA:CameraSettings": lambda x: _read_cam_settings(x),
    "TAGame.PRI_TA:ClientLoadout": lambda x: _read_loadout(x),
    "TAGame.Car_TA:TeamPaint": lambda x: _read_teampaint(x),
    "TAGame.Ball_TA:ReplicatedExplosionData": lambda x: _read_explosion(x),
    "Engine.Actor:Role": lambda x: _read_enum(x),
    "Engine.Actor:Location": lambda x: _read_location(x),
    "TAGame.CarComponent_Dodge_TA:DodgeTorque": lambda x: _read_location(x),
    "ProjectX.GRI_X:GameServerID": lambda x: _read_qword(x),
    "ProjectX.GRI_X:Reservations": lambda x: _read_reservations(x),
    "TAGame.VehiclePickup_TA:ReplicatedPickupData": lambda x: _read_pickup(x),
    "TAGame.Car_TA:ReplicatedDemolish": lambda x: _read_demolish(x),
    "TAGame.GameEvent_Soccar_TA:ReplicatedMusicStinger": lambda x: _read_musicstinger(x)
}


def read_property_value(property_name, bitstream):
    try:
        value = parsing[property_name](bitstream)
    except KeyError:
        raise PropertyParsingError("Dont know how to parse bits for %s Have some raw Bits: %s"
                                   % (property_name, bitstream.read('hex:64')))
    return value


def _read_flagged_int(bitstream):
    flag = bitstream.read(BOOL)
    num = _read_int(bitstream)
    return flag, num


def _read_int(bitstream):
    return reverse_bytewise(bitstream.read('bits:32')).intle


def _read_byte(bitstream):
    return reverse_bytewise(bitstream.read('bits:8')).uintle


def _read_bool(bitstream):
    return bitstream.read(BOOL)


def _read_float(bitstream):
    return reverse_bytewise(bitstream.read('bits:32')).floatle


def _read_string(bitstream):  # This should be in utils. But its only needed here, so yeah
    length = _read_int(bitstream)*8
    if length < 0:
        length *= -2
        return reverse_bytewise(bitstream.read('bits:'+str(length))).bytes[:-2].decode('utf-16')
    return reverse_bytewise(bitstream.read('bits:'+str(length))).bytes[:-1].decode('utf-8')


def _read_rigid_body_state(bitstream):
    flag = bitstream.read(BOOL)
    position = read_serialized_vector(bitstream)
    rotation = read_float_vector(bitstream)
    result = {'flag': flag,
              'pos': position,
              'rot': rotation}
    if not flag:  # Totally not sure about this
        result['vec1'] = read_serialized_vector(bitstream)
        result['vec2'] = read_serialized_vector(bitstream)
    return result


def _read_unique_id(bitstream):
    system = _read_byte(bitstream)
    if system == 0:  # Splitscreen
        uid = reverse_bytewise(bitstream.read('bits:24')).uintle
    elif system == 1:  # STEAM
        uid = reverse_bytewise(bitstream.read('bits:64')).uintle
    elif system == 2:  # PS4
        uid = reverse_bytewise(bitstream.read('bits:256')).hex
    else:
        raise PropertyParsingError('Unknown System ID')
    splitscreen_id = _read_byte(bitstream)
    return system, uid, splitscreen_id


def _read_cam_settings(bitstream):
    return {
        'fov': _read_float(bitstream),
        'height': _read_float(bitstream),
        'pitch': _read_float(bitstream),
        'dist': _read_float(bitstream),
        'stiff': _read_float(bitstream),
        'swiv': _read_float(bitstream)
    }


def _read_loadout(bitstream):
    # Loadout has no Paint information, could be Car, Decal?, Wheels, Boost, Hat, Antenna, Title
    index = _read_byte(bitstream)
    values = [_read_int(bitstream) for i in range(7)]
    return index, values


def _read_teampaint(bitstream):
    return {
        "Team": _read_byte(bitstream),
        "TeamColorID": _read_byte(bitstream),
        "CustomColorID": _read_byte(bitstream),
        "TeamFinishID": _read_int(bitstream),
        "CustomFinishID": _read_int(bitstream),
    }


def _read_pickup(bitstream):
    # Seems quirky but yields good results... let it rest for now son
    instigator = _read_bool(bitstream)
    if instigator:
        # print("instigator present")
        return _read_int(bitstream), _read_bool(bitstream)  # InstigatorId + picked up
    # print("no instigator?")
    return _read_bool(bitstream)  # Only picked up


def _read_explosion(bitstream):
    nogoal = _read_bool(bitstream)
    if nogoal:
        return nogoal, read_serialized_vector(bitstream)
    return nogoal, _read_int(bitstream), read_serialized_vector(bitstream)


def _read_enum(bitstream):
    # What? O_o it seems right, but why 11? Like...what?
    return reverse_bytewise(bitstream.read('bits:11')).hex


def _read_location(bitstream):
    return read_serialized_vector(bitstream)


def _read_qword(bitstream):
    return _read_int(bitstream), _read_int(bitstream)


def _read_reservations(bitstream):
    unknown = reverse_bytewise(bitstream.read('bits:3')).hex
    system, uid, playernum = _read_unique_id(bitstream)
    name = "Not Set"
    if system != 0:
        name = _read_string(bitstream)
    flag_1 = _read_bool(bitstream)
    flag_2 = _read_bool(bitstream)
    return unknown, name, flag_1, flag_2


def _read_demolish(bitstream):
    result = {}
    atk_present = _read_bool(bitstream)
    result['atk'] = _read_int(bitstream)
    vic_present = _read_bool(bitstream)
    result['vic'] = _read_int(bitstream)
    result['atk_vec'] = read_serialized_vector(bitstream)
    result['atk_vec'] = read_serialized_vector(bitstream)
    return result


def _read_musicstinger(bitstream):
    flag = _read_bool(bitstream)
    soundcue = _read_int(bitstream)
    trigger = _read_byte(bitstream)
    return soundcue, trigger
