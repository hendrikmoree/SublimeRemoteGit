on run argv
    if count of argv is 3 then
        set command to item 1 of argv
        set pkgname to item 2 of argv
        set pkgversion to item 3 of argv
    end if

    tell application "/Applications/iTerm.app"
        if (exists current window) then
            tell current window to create tab with default profile
        else
            create window with default profile
        end if
        tell current session of current window
            write text command & " " & pkgname & " " & pkgversion
        end tell
        activate
    end tell
end run