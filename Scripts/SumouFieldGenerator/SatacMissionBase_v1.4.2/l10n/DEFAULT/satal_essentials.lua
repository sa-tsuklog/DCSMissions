----------------------------------------------------
-------------------PRECONDITIONS--------------------
--以下の機能を提供する。
----1. ミッションの終了メッセージ
----2. ラジオメニューによるAWACSの無効化
----3. バブル判定
--
--使用方法
----ミッション開始時と各時間ステップでsatal_essentialsを呼び出す
----バブルはNeutralのBullseye位置とする
--
--フラグ
FLAG_ID_NM_INITIAL_BUBBLE_SIZE = '1'
FLAG_ID_S_BUBBLE_SHRINK_TIME = '2'

FLAG_ID_INITIALIZED = '10'
FLAG_ID_MISSION_END_TIME = '11'
FLAG_ID_MISSION_END_REQUEST = '12'
FLAG_ID_MISSION_PROLONGED = '13'

FLAG_ID_TIME_TO_BUBBLE_ACTIVE = '20'
FLAG_ID_TIME_TO_BUBBLE_SHRINK = '21'
FLAG_ID_BUBBLE_RESET_TIMEOUT = '22'
FLAG_ID_NM_BUBBLE_SIZE = '23'
FLAG_ID_COMBAT_START_TIME = '24'
FLAG_ID_COMBAT_END_TIME = '25'
FLAG_ID_NUM_BLUE_PLAYERS_IN_INNER_BUBBLE = '26'
FLAG_ID_NUM_BLUE_PLAYERS_AT_BUFFER_ZONE = '27'
FLAG_ID_NUM_BLUE_PLAYERS_OUT_OF_OUTER_BUBBLE = '28'
FLAG_ID_NUM_RED_PLAYERS_IN_INNER_BUBBLE = '29'
FLAG_ID_NUM_RED_PLAYERS_AT_BUFFER_ZONE = '30'
FLAG_ID_NUM_RED_PLAYERS_OUT_OF_OUTER_BUBBLE = '31'
FLAG_ID_OUT_OF_BUFFER_ZONE_SOUND = '32'
FLAG_ID_OUT_OF_BUBBLE_SOUND = '33'
FLAG_ID_BUBBLE_SHRINK_SOUND = '34'
----------------------------------------------------


S_BUBBLE_ACTIVE_DELAY = 30
S_DEFAULT_MISSION_END_TIME = 10800
BUBBLE_RESET_DELAY = 10

function prolongMissionTime()
    local missionEndTime = trigger.misc.getUserFlag(FLAG_ID_MISSION_END_TIME)
    trigger.action.setUserFlag(FLAG_ID_MISSION_END_TIME,missionEndTime + 1800)
    trigger.action.setUserFlag(FLAG_ID_MISSION_PROLONGED,5)
    trigger.action.outText("Mission ends in ".. math.ceil((missionEndTime + 1800 - timer.getTime())/60) .."minute", 1,false)
end

function missionEndRequest()
    trigger.action.setUserFlag(FLAG_ID_MISSION_END_REQUEST,1)
end

function bubbleShrink()
    local nmBubbleSize = trigger.misc.getUserFlag(FLAG_ID_NM_BUBBLE_SIZE)
    if(nmBubbleSize > 2)then
        trigger.action.setUserFlag(FLAG_ID_NM_BUBBLE_SIZE,nmBubbleSize-1)
    end
end

function deactivateAwacs()
    for groupId,groupData in pairs(mist.DBs.groupsByName)do
        if(groupData.task == "AWACS")then
            Group.getByName(groupData.groupName):destroy()
            trigger.action.outText(groupData.groupName.." deactivated.", 1,false)
        end
    end
end

function initialize()
    --mission time
    trigger.action.setUserFlag(FLAG_ID_MISSION_END_TIME,S_DEFAULT_MISSION_END_TIME)

    missionCommands.addCommand("Prolong 30 minutes",nil,prolongMissionTime)
    missionCommands.addCommand("End mission",nil,missionEndRequest)

    --bubble
    local nmInitialBubbleSize = trigger.misc.getUserFlag(FLAG_ID_NM_INITIAL_BUBBLE_SIZE)
    local sBubbleShrinkTime = trigger.misc.getUserFlag(FLAG_ID_S_BUBBLE_SHRINK_TIME)

    trigger.action.setUserFlag(FLAG_ID_TIME_TO_BUBBLE_ACTIVE,S_BUBBLE_ACTIVE_DELAY)
    trigger.action.setUserFlag(FLAG_ID_NM_BUBBLE_SIZE,nmInitialBubbleSize)
    trigger.action.setUserFlag(FLAG_ID_TIME_TO_BUBBLE_SHRINK,sBubbleShrinkTime)

    missionCommands.addCommand("Bubble shrink",nil,bubbleShrink)


    missionCommands.addCommand("Deactivate AWACS",nil,deactivateAwacs)

    trigger.action.setUserFlag(FLAG_ID_INITIALIZED,1)
end

function missionTimeManagement()
    local missionEndTime = trigger.misc.getUserFlag(FLAG_ID_MISSION_END_TIME)
    local missionProlonged = trigger.misc.getUserFlag(FLAG_ID_MISSION_PROLONGED)

    if(math.floor(timer.getTime()) == missionEndTime)then
        trigger.action.setUserFlag(FLAG_ID_MISSION_END_REQUEST,1)
    elseif((math.floor(timer.getTime()) >= (missionEndTime - 300)) or (missionProlonged > 0))then
        trigger.action.outText("Mission ends in ".. math.ceil((missionEndTime - timer.getTime())/60) .."minute", 1,false)
    end

    if(missionProlonged > 0)then
        trigger.action.setUserFlag(FLAG_ID_MISSION_PROLONGED,missionProlonged - 1)
    end
end

function bubbleManagement()
    local nmInitialBubbleSize = trigger.misc.getUserFlag(FLAG_ID_NM_INITIAL_BUBBLE_SIZE)
    local sBubbleShrinkTime = trigger.misc.getUserFlag(FLAG_ID_S_BUBBLE_SHRINK_TIME)
    local bubbleActiveCount = trigger.misc.getUserFlag(FLAG_ID_TIME_TO_BUBBLE_ACTIVE)
    local bubbleShrinkCount = trigger.misc.getUserFlag(FLAG_ID_TIME_TO_BUBBLE_SHRINK)
    local bubbleResetTimeout = trigger.misc.getUserFlag(FLAG_ID_BUBBLE_RESET_TIMEOUT)
    local nmBubbleSize = trigger.misc.getUserFlag(FLAG_ID_NM_BUBBLE_SIZE)
    local numBluePlayersInInnerBubble = trigger.misc.getUserFlag(FLAG_ID_NUM_BLUE_PLAYERS_IN_INNER_BUBBLE)
    local numBluePlayersAtBufferZone = trigger.misc.getUserFlag(FLAG_ID_NUM_BLUE_PLAYERS_AT_BUFFER_ZONE)
    local numBluePlayersOutOfOuterBubble = trigger.misc.getUserFlag(FLAG_ID_NUM_BLUE_PLAYERS_OUT_OF_OUTER_BUBBLE)
    local numRedPlayersInInnerBubble = trigger.misc.getUserFlag(FLAG_ID_NUM_RED_PLAYERS_IN_INNER_BUBBLE)
    local numRedPlayersAtBufferZone = trigger.misc.getUserFlag(FLAG_ID_NUM_RED_PLAYERS_AT_BUFFER_ZONE)
    local numRedPlayersOutOfOuterBubble = trigger.misc.getUserFlag(FLAG_ID_NUM_RED_PLAYERS_OUT_OF_OUTER_BUBBLE)
    local combatStartTime = trigger.misc.getUserFlag(FLAG_ID_COMBAT_START_TIME)
    local combatEndTime = trigger.misc.getUserFlag(FLAG_ID_COMBAT_END_TIME)

    trigger.action.setUserFlag(FLAG_ID_OUT_OF_BUFFER_ZONE_SOUND, false) --out of buffer zone sound
    trigger.action.setUserFlag(FLAG_ID_OUT_OF_BUBBLE_SOUND, false) --out of bubble sound
    trigger.action.setUserFlag(FLAG_ID_BUBBLE_SHRINK_SOUND, false)

    local mBubblePos = coalition.getMainRefPoint(coalition.side.NEUTRAL)

    local bluePlayerNamesOutOfOuterBubble = {}
    local bluePlayerNamesAtBufferZone = {}
    local bluePlayerNamesInInnerBubble = {}
    local redPlayerNamesOutOfOuterBubble = {}
    local redPlayerNamesAtBufferZone = {}
    local redPlayerNamesInInnerBubble = {}

    local mBubbleSize = mist.utils.NMToMeters(nmBubbleSize)
    local mBufferZoneSize = mist.utils.NMToMeters(nmBubbleSize - 2.5)
    

    -------------------------------------------------------------
    --Bubble外、バッファーゾーン外、バッファーゾーン内の人数を計測
    -------------------------------------------------------------
    for clientId, clientData in pairs(mist.DBs.humansById) do
        local unit = Unit.getByName(clientData.unitName)
        if unit ~= nil then
            local p1 = unit:getPosition().p
            local mDistance = mist.utils.get2DDist(mBubblePos,p1)
            
            if (mDistance > mBubbleSize) then
                if(clientData.coalition == "blue")then
                    bluePlayerNamesOutOfOuterBubble[#bluePlayerNamesOutOfOuterBubble+1] = unit:getPlayerName()
                elseif(clientData.coalition == "red")then
                    redPlayerNamesOutOfOuterBubble[#redPlayerNamesOutOfOuterBubble+1] = unit:getPlayerName()
                end
            elseif(mDistance > mBufferZoneSize) then
                if(clientData.coalition == "blue")then
                    bluePlayerNamesAtBufferZone[#bluePlayerNamesAtBufferZone+1] = unit:getPlayerName()
                elseif(clientData.coalition == "red")then
                    redPlayerNamesAtBufferZone[#redPlayerNamesAtBufferZone+1] = unit:getPlayerName()
                end
            else
                if(clientData.coalition == "blue")then
                    bluePlayerNamesInInnerBubble[#bluePlayerNamesInInnerBubble+1] = unit:getPlayerName()
                elseif(clientData.coalition == "red")then
                    redPlayerNamesInInnerBubble[#redPlayerNamesInInnerBubble+1] = unit:getPlayerName()
                end
            end
        end
    end

    -------------------------------------------------------------
    --タイマーアップデート
    -------------------------------------------------------------
    if(((#bluePlayerNamesAtBufferZone == 0) and (#bluePlayerNamesInInnerBubble == 0)) and ((#redPlayerNamesAtBufferZone == 0) and (#redPlayerNamesInInnerBubble == 0)))then  --バブル内にプレイヤー無し
        if(bubbleResetTimeout == 0)then
            bubbleActiveCount = S_BUBBLE_ACTIVE_DELAY
            nmBubbleSize = nmInitialBubbleSize
            bubbleShrinkCount = sBubbleShrinkTime
        else
            bubbleResetTimeout = bubbleResetTimeout - 1
        end
    else    --バブル内にプレイヤー有り
        bubbleResetTimeout = BUBBLE_RESET_DELAY
        if(bubbleActiveCount ~= 0)then --未アクティブ
            bubbleActiveCount = bubbleActiveCount - 1
        else
            if(sBubbleShrinkTime > 0)then
                if(bubbleShrinkCount == 1)then
                    bubbleShrinkCount = sBubbleShrinkTime
                    if(nmBubbleSize > 1)then
                        nmBubbleSize = nmBubbleSize - 1
                    end
                    trigger.action.setUserFlag(FLAG_ID_BUBBLE_SHRINK_SOUND,true)
                else
                    bubbleShrinkCount = bubbleShrinkCount - 1
                end
            end
        end
    end

    --trigger.action.outText("out of bubble=" ..#bluePlayerNamesOutOfOuterBubble..", in buffer zone="..#bluePlayerNamesAtBufferZone..", in bubble"..#bluePlayerNamesInInnerBubble, 10,false)
    trigger.action.outText("Blue [0:0] Red(1st Half) CZ Radius: ".. nmBubbleSize.."nm TTS: "..bubbleShrinkCount, 1,true)

    -------------------------------------------------------------
    --メッセージ表示 バブル関連
    -------------------------------------------------------------
    if(bubbleActiveCount ~= 0)then
        if(#bluePlayerNamesAtBufferZone + #bluePlayerNamesInInnerBubble > 0)then
            local names = ""
            for id,name in pairs(bluePlayerNamesInInnerBubble) do
                names = name .. ", " .. names
            end 
            for id, name in pairs(bluePlayerNamesAtBufferZone) do
                names = name .. ", " .. names
            end
            trigger.action.outText("Entered CombatZone(blue): " .. names, 1,false)
        end

        if(#redPlayerNamesAtBufferZone + #redPlayerNamesInInnerBubble > 0)then
            local names = ""
            for id,name in pairs(redPlayerNamesInInnerBubble) do
                names = name .. ", " .. names
            end 
            for id, name in pairs(redPlayerNamesAtBufferZone) do
                names = name .. ", " .. names
            end
            trigger.action.outText("Entered CombatZone(red): " .. names, 1,false)
        end
    else
        if (#bluePlayerNamesAtBufferZone > 0)then
            local names = ""
            for id,name in pairs(bluePlayerNamesAtBufferZone) do
                names = name .. ", " .. names
            end
            trigger.action.outText("WARNING! Leaving CombatZone(blue): " .. names, 1,false)
        end
        if (#redPlayerNamesAtBufferZone > 0)then
            local names = ""
            for id,name in pairs(redPlayerNamesAtBufferZone) do
                names = name .. ", " .. names
            end
            trigger.action.outText("WARNING! Leaving CombatZone(red): " .. names, 1,false)
        end

        if (#bluePlayerNamesOutOfOuterBubble > 0)then
            local names = ""
            for id,name in pairs(bluePlayerNamesOutOfOuterBubble) do
                names = name .. ", " .. names
            end
            trigger.action.outText("Out Of CombatZone(blue): " .. names, 1,false)
        end
        if (#redPlayerNamesOutOfOuterBubble > 0)then
            local names = ""
            for id,name in pairs(redPlayerNamesOutOfOuterBubble) do
                names = name .. ", " .. names
            end
            trigger.action.outText("Out Of CombatZone(red): " .. names, 1,false)
        end

        if((#bluePlayerNamesAtBufferZone > numBluePlayersAtBufferZone) or (#redPlayerNamesAtBufferZone > numRedPlayersAtBufferZone))then
            trigger.action.setUserFlag(FLAG_ID_OUT_OF_BUFFER_ZONE_SOUND, true)
        end
        if((#bluePlayerNamesOutOfOuterBubble > numBluePlayersOutOfOuterBubble) or (#redPlayerNamesOutOfOuterBubble > numRedPlayersOutOfOuterBubble))then
            trigger.action.setUserFlag(FLAG_ID_OUT_OF_BUBBLE_SOUND,true)
        end
    end

    -------------------------------------------------------------
    --メッセージ表示 戦闘終了
    -------------------------------------------------------------
    local numBluePlayersInOuterBubble = numBluePlayersAtBufferZone + numBluePlayersInInnerBubble
    local numRedPlayersInOuterBubble = numRedPlayersAtBufferZone + numRedPlayersInInnerBubble
    if((numBluePlayersInOuterBubble + numRedPlayersInOuterBubble == 0) and (#bluePlayerNamesAtBufferZone + #bluePlayerNamesInInnerBubble + #redPlayerNamesAtBufferZone + # redPlayerNamesInInnerBubble > 0))then
        combatStartTime = math.floor(timer.getTime())
    end
    if((numBluePlayersInOuterBubble > 0 and numRedPlayersInOuterBubble > 0) and ((#bluePlayerNamesAtBufferZone + #bluePlayerNamesInInnerBubble ==0) or (#redPlayerNamesAtBufferZone + #redPlayerNamesInInnerBubble == 0)))then
        combatEndTime = math.floor(timer.getTime())
    end

    if(math.floor(timer.getTime()) - combatEndTime < 10)then
        local combatTime = combatEndTime-combatStartTime
        trigger.action.outText("Combat ended in " .. combatTime .. " [sec]", 1,false)
    end

    
    trigger.action.setUserFlag(FLAG_ID_TIME_TO_BUBBLE_ACTIVE,bubbleActiveCount)
    trigger.action.setUserFlag(FLAG_ID_TIME_TO_BUBBLE_SHRINK,bubbleShrinkCount)
    trigger.action.setUserFlag(FLAG_ID_BUBBLE_RESET_TIMEOUT,bubbleResetTimeout)
    trigger.action.setUserFlag(FLAG_ID_NM_BUBBLE_SIZE,nmBubbleSize)
    trigger.action.setUserFlag(FLAG_ID_NUM_BLUE_PLAYERS_IN_INNER_BUBBLE,#bluePlayerNamesInInnerBubble)
    trigger.action.setUserFlag(FLAG_ID_NUM_BLUE_PLAYERS_AT_BUFFER_ZONE,#bluePlayerNamesAtBufferZone)
    trigger.action.setUserFlag(FLAG_ID_NUM_BLUE_PLAYERS_OUT_OF_OUTER_BUBBLE,#bluePlayerNamesOutOfOuterBubble)
    trigger.action.setUserFlag(FLAG_ID_NUM_RED_PLAYERS_IN_INNER_BUBBLE,#redPlayerNamesInInnerBubble)
    trigger.action.setUserFlag(FLAG_ID_NUM_RED_PLAYERS_AT_BUFFER_ZONE,#redPlayerNamesAtBufferZone)
    trigger.action.setUserFlag(FLAG_ID_NUM_RED_PLAYERS_OUT_OF_OUTER_BUBBLE,#redPlayerNamesOutOfOuterBubble)
    trigger.action.setUserFlag(FLAG_ID_COMBAT_START_TIME,combatStartTime)
    trigger.action.setUserFlag(FLAG_ID_COMBAT_END_TIME,combatEndTime)
end


do
    --trigger.action.outText("active = "..bubbleActiveCount..", shrink = "..bubbleShrinkCount..", BubbleSize = "..nmBubbleSize, 1,false)

    if(trigger.misc.getUserFlag(FLAG_ID_INITIALIZED) == 0)then
        initialize()
    end
    bubbleManagement()
    missionTimeManagement()
end