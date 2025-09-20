do
    local flagVal = trigger.misc.getUserFlag('1')
    trigger.action.outText("Message sample flag1 = ".. flagVal.." [s]", 1,true)
end