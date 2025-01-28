# $0$ Cache type
#
ruleset adr:Address do
    liveness "$0$ is able to eventually read" live_$0$(adr, load);
    liveness "$0$ is able to eventually write" live_$0$(adr, load);
endruleset;
