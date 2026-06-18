
// Gets the number of months between two Date objects
function getMonthGap(biggerDate, smallerDate) 
{
    tbigmonths = biggerDate.getMonth() + 1 + biggerDate.getYear() * 12
    tsmallmonths = smallerDate.getMonth() + 1 + smallerDate.getYear() * 12
    monthGap = tbigmonths - tsmallmonths

    return monthGap
}

// Gets a readable string of gap between two Date objects
function getReadableString(tbig, tsmall) {
    let seconds = (tbig.getTime() - tsmall.getTime()) / 1000.0
    // within minute, give seconds
    if (seconds < 60.0)
        return seconds + " seconds ago"
    
    // within hour, give minutes
    minutes = seconds / 60.0
    if (minutes < 60.0)
        return Math.round(minutes) + ((Math.round(minutes) <= 1) ? " minute ago" : " minutes ago")

    // within day, give hours
    hours = minutes / 60.0
    if (hours < 24.0)
        return Math.round(hours) + ((Math.round(hours) <= 1) ? " hour ago" : " hours ago")
    
    // within week, give days
    days = hours / 24.0
    if (days < 7)
        return Math.round(days) + ((Math.round(days) <= 1) ? " day ago" : " days ago")
    
    // within within a month, give weeks
    weeks = days / 7.0
    if (weeks < 4)
        return Math.round(weeks) + ((Math.round(weeks) <= 1) ? " week ago" : " weeks ago")
    
    // within a year, give months
    let months = getMonthGap(tbig, tsmall)
    if (months < 12.0)
        return Math.round(months) + ((Math.round(months) <= 1) ? " month ago" : " months ago")

    // give years
    let years = months / 12.0
    return Math.round(years) + ((Math.round(years) <= 1) ? " year ago" : " years ago")
}



/** @type {string} */
let mtime = document.getElementById("content").childNodes[1].childNodes[1].innerText + ""

// by default, assume there is no commit.
mtime = mtime.slice("last modified: (".length, -1)
let readableTime = "new"

if (mtime != "no commit") {
    
    let mtimeDate = new Date(mtime)
    let currentTime = new Date()
    
    readableTime = getReadableString(currentTime, mtimeDate)
}

document.getElementById("content").childNodes[1].childNodes[1].innerHTML = "<em>last modified: " + readableTime + " (" + mtime + ")</em>"