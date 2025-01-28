# $0$ Cache type
#
ruleset n:OBJSET_$0$ do
    ruleset adr:Address do
        liveness "$0$ is able to eventually read" g_perm.$0$[n][adr][load];
        liveness "$0$ is able to eventually write" g_perm.$0$[n][adr][store];
    endruleset;
endruleset;
