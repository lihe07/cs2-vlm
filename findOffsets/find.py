import os
import re
import subprocess
import win32api as wapi
import win32api
import win32gui
import win32process

# Define the folder to search
folder_path = 'C:/Users/Bruno Chen/Downloads/output/'


def run_cs2_dumper():
    try:
        result = subprocess.run(['findOffsets\cs2-dumper.exe'])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running cs2-dumpe.exe: {e}")

# Check if CS2 is running by checkign if there is a cs2 window
hwin = win32gui.FindWindow(None, "Counter-Strike 2")

if(hwin == 0):
    print("CS2 is not running")
else:
    print("CS2 is running")
    

        
# Run cs2-dumpe.exe to dump the offsets
run_cs2_dumper()


# Define the variables to update
variables_to_update = {
    "anim_overlays",
    "clientstate_choked_commands",
    "clientstate_delta_ticks",
    "clientstate_last_outgoing_command",
    "clientstate_net_channel",
    "convar_name_hash_table",
    "dwClientState",
    "dwClientState_GetLocalPlayer",
    "dwClientState_IsHLTV",
    "dwClientState_Map",
    "dwClientState_MapDirectory",
    "dwClientState_MaxPlayer",
    "dwClientState_PlayerInfo",
    "dwClientState_State",
    "dwClientState_ViewAngles",
    "dwEntityList",
    "dwForceAttack",
    "dwForceAttack2",
    "dwForceBackward",
    "dwForceForward",
    "dwForceJump",
    "dwForceLeft",
    "dwForceRight",
    "dwGameDir",
    "dwGameRulesProxy",
    "dwGetAllClasses",
    "dwGlobalVars",
    "dwGlowObjectManager",
    "dwInput",
    "dwInterfaceLinkList",
    "dwLocalPlayer",
    "dwMouseEnable",
    "dwMouseEnablePtr",
    "dwPlayerResource",
    "dwRadarBase",
    "dwSensitivity",
    "dwSensitivityPtr",
    "dwSetClanTag",
    "dwViewMatrix",
    "dwWeaponTable",
    "dwWeaponTableIndex",
    "dwYawPtr",
    "dwZoomSensitivityRatioPtr",
    "dwbSendPackets",
    "dwppDirect3DDevice9",
    "find_hud_element",
    "force_update_spectator_glow",
    "interface_engine_cvar",
    "is_c4_owner",
    "m_bDormant",
    "m_bIsLocalPlayer",
    "m_flSpawnTime",
    "m_pStudioHdr",
    "m_pitchClassPtr",
    "m_yawClassPtr",
    "model_ambient_min",
    "set_abs_angles",
    "set_abs_origin",
    "cs_gamerules_data",
    "m_ArmorValue",
    "m_Collision",
    "m_CollisionGroup",
    "m_Local",
    "m_MoveType",
    "m_OriginalOwnerXuidHigh",
    "m_OriginalOwnerXuidLow",
    "m_SurvivalGameRuleDecisionTypes",
    "m_SurvivalRules",
    "m_aimPunchAngle",
    "m_aimPunchAngleVel",
    "m_angEyeAnglesX",
    "m_angEyeAnglesY",
    "m_bBombDefused",
    "m_bBombPlanted",
    "m_bBombTicking",
    "m_bFreezePeriod",
    "m_bGunGameImmunity",
    "m_bHasDefuser",
    "m_bHasHelmet",
    "m_bInReload",
    "m_bIsDefusing",
    "m_bIsQueuedMatchmaking",
    "m_bIsScoped",
    "m_bIsValveDS",
    "m_bSpotted",
    "m_bSpottedByMask",
    "m_bStartedArming",
    "m_bUseCustomAutoExposureMax",
    "m_bUseCustomAutoExposureMin",
    "m_bUseCustomBloomScale",
    "m_clrRender",
    "m_dwBoneMatrix",
    "m_fAccuracyPenalty",
    "m_fFlags",
    "m_flC4Blow",
    "m_flCustomAutoExposureMax",
    "m_flCustomAutoExposureMin",
    "m_flCustomBloomScale",
    "m_flDefuseCountDown",
    "m_flDefuseLength",
    "m_flFallbackWear",
    "m_flFlashDuration",
    "m_flFlashMaxAlpha",
    "m_flLastBoneSetupTime",
    "m_flLowerBodyYawTarget",
    "m_flNextAttack",
    "m_flNextPrimaryAttack",
    "m_flSimulationTime",
    "m_flTimerLength",
    "m_hActiveWeapon",
    "m_hBombDefuser",
    "m_hMyWeapons",
    "m_hObserverTarget",
    "m_hOwner",
    "m_hOwnerEntity",
    "m_hViewModel",
    "m_iAccountID",
    "m_iClip1",
    "m_iCompetitiveRanking",
    "m_iCompetitiveWins",
    "m_iCrosshairId",
    "m_iDefaultFOV",
    "m_iEntityQuality",
    "m_iFOV",
    "m_iFOVStart",
    "m_iGlowIndex",
    "m_iHealth",
    "m_iItemDefinitionIndex",
    "m_iItemIDHigh",
    "m_iMostRecentModelBoneCounter",
    "m_iObserverMode",
    "m_iShotsFired",
    "m_iState",
    "m_iTeamNum",
    "m_lifeState",
    "m_nBombSite",
    "m_nFallbackPaintKit",
    "m_nFallbackSeed",
    "m_nFallbackStatTrak",
    "m_nForceBone",
    "m_nModelIndex",
    "m_nTickBase",
    "m_nViewModelIndex",
    "m_rgflCoordinateFrame",
    "m_szCustomName",
    "m_szLastPlaceName",
    "m_thirdPersonViewAngles",
    "m_vecOrigin",
    "m_vecVelocity",
    "m_vecViewOffset",
    "m_viewPunchAngle",
    "m_zoomLevel"
}

# Function to find the decimal values
def find_decimal_values(folder_path, variables):
    results = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):  # Assuming the files are .json
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    for var in variables:
                        match = re.search(rf'"{var}": (\d+)', content)
                        if match:
                            results[var] = match.group(1)
    return results

# Find the decimal values
decimal_values = find_decimal_values(folder_path, variables_to_update)

# Write the results to a file
with open('outputOffsets.py', 'w') as f:
    f.write('#signatures\n\n')
    for var, value in decimal_values.items():
        f.write(f'{var} = {value}\n')