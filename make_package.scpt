on run argv
    if count of argv is 3 then
        set command to item 1 of argv
        set pkgname to item 2 of argv
        set pkgversion to item 3 of argv
    end if

    tell application "iTerm"
        activate

        set _term to (make new terminal)

        tell _term
            launch session "Default Session"
            set _session to current session
        end tell

        tell _session
            write text command & " " & pkgname & " " & pkgversion
        end tell
    end tell
end run