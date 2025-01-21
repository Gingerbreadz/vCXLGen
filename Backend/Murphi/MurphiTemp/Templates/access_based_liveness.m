# $0$ Cache entity
#
ruleset adr:Address do
    liveness "$0$ is able to eventually read" g_perm[m_$0$][adr][load];
    liveness "$0$ is able to eventually write" g_perm[m_$0$][adr][store];
endruleset;