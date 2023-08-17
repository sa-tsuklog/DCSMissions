do
    local bubbleActiveCount = trigger.misc.getUserFlag('60')
    local bubbleShrinkCount = trigger.misc.getUserFlag('61')
    local nmBubbleSize = trigger.misc.getUserFlag('62')
    trigger.action.setUserFlag('63', false)

    --trigger.action.outText("active = "..bubbleActiveCount..", shrink = "..bubbleShrinkCount..", BubbleSize = "..nmBubbleSize, 1,false)

    local mBubblePos = trigger.misc.getZone('Bubble').point

    local playerNamesOutOfBubble = {}
    local playerNamesOutOfBufferZone = {}
    local playerNamesInBufferZone = {}

    local mBubbleSize = mist.utils.NMToMeters(nmBubbleSize)
    local mBufferZoneSize = mist.utils.NMToMeters(nmBubbleSize - 2.5)
    --trigger.action.outText("Flag60 = " .. flag60 .. ", Flag61=" .. flag61 .. ", Flag62=" .. flag62,10,true)
    for clientId, clientData in pairs(mist.DBs.humansById) do
        local unit = Unit.getByName(clientData.unitName)
        if unit ~= nil then
            local p1 = unit:getPosition().p
            local mDistance = mist.utils.get2DDist(mBubblePos,p1)
            -- trigger.action.outText("dist2d=" .. mDistance .. "p1=("..p1.x..","..p1.y..")", 10,false)
            -- trigger.action.outText("player name = " .. unit:getPlayerName(), 10,false)
            
            if (mDistance > mBubbleSize) then
                playerNamesOutOfBubble[#playerNamesOutOfBubble+1] = unit:getPlayerName()
                -- trigger.action.outText("player" ..unit:getPlayerName().." is out of bubble. id="..clientData.unitId, 10,false)

            elseif(mDistance > mBufferZoneSize) then
                playerNamesOutOfBufferZone[#playerNamesOutOfBufferZone+1] = unit:getPlayerName()
                -- trigger.action.outText("player" ..unit:getPlayerName().." is in buffer zone. id="..clientData.unitId, 10,false)
            else
                playerNamesInBufferZone[#playerNamesInBufferZone+1] = unit:getPlayerName()
                -- trigger.action.outText("player" ..unit:getPlayerName().." is in bubble. id="..clientData.unitId, 10,false)
            end
        end
    end

    -- trigger.action.outText("out of bubble=" ..#playerNamesOutOfBubble..", in buffer zone="..#playerNamesOutOfBufferZone..", in bubble"..#playerNamesInBufferZone, 10,false)

    if(bubbleActiveCount ~= 0)then
        if(#playerNamesOutOfBufferZone + #playerNamesInBufferZone > 0)then
            local names = ""
            for id,name in pairs(playerNamesInBufferZone) do
                names = name .. ", " .. names
            end 
            for id, name in pairs(playerNamesOutOfBufferZone) do
                names = name .. ", " .. names
            end
            trigger.action.outText(names.." entered bubble", 1,false)
        end
    else
        if (#playerNamesOutOfBufferZone > 0)then
            local names = ""
            for id,name in pairs(playerNamesOutOfBufferZone) do
                names = name .. ", " .. names
            end
            trigger.action.outText(names.." are near to bubble edge", 1,false)
            trigger.action.setUserFlag('63', true)
        end

        if (#playerNamesOutOfBubble > 0)then
            local names = ""
            for id,name in pairs(playerNamesOutOfBubble) do
                names = name .. ", " .. names
            end
            trigger.action.outText(names.." are out of bubble", 1,false)
            trigger.action.setUserFlag('63', true)
        end

    end    
end