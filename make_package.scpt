on run argv
    if count of argv is 3 then
        set command to item 1 of argv
        set pkgname to item 2 of argv
        set pkgversion to item 3 of argv
    end if

    tell application "iTerm2"
        tell current window
            set newTab to (create tab with default profile)
            tell current session
                write text command & " " & pkgname & " " & pkgversion
            end tell
        end tell
    end tell
end run