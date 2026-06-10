"""Course-local replacement for pl-code with proper syntax highlighting for the
three assembly dialects used in this course (as accepted by llvm-mc):

    <asm-code language="arm64">...</asm-code>   ARM64 GAS
    <asm-code language="arm32">...</asm-code>   ARM32/Thumb GAS
    <asm-code language="x64">...</asm-code>     x86-64 Intel syntax

Like pl-code, inline content is parsed as HTML, so a literal "<" must be
written as "&lt;".

The regex constants in the GENERATED block below are extracted from capstone's
instruction/register/condition-code enumerations by:

    python -m util generate_highlighting

Do not edit that block by hand. Token colors are kept consistent with the
custom ace modes in clientFilesCourse/ace/mode/ (same generator).
"""

import re
from functools import cache
from html import unescape

import chevron
import lxml.html
import prairielearn as pl
import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexer import RegexLexer
from pygments.styles import STYLE_MAP, get_style_by_name
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)

STYLE_NAME_DEFAULT = "dracula"

# BEGIN GENERATED (python -m util generate_highlighting) -- do not edit by hand
ARM64_MNEMONICS = 'b\\.(?:al|cc|cs|eq|ge|gt|hi|hs|le|lo|ls|lt|mi|ne|nv|pl|vc|vs)|(?:autia1716|autib1716|cpyfertrn|cpyfertwn|cpyfewtrn|cpyfewtwn|cpyfmrtrn|cpyfmrtwn|cpyfmwtrn|cpyfmwtwn|cpyfprtrn|cpyfprtwn|cpyfpwtrn|cpyfpwtwn|ldsmaxalb|ldsmaxalh|ldsminalb|ldsminalh|ldumaxalb|ldumaxalh|lduminalb|lduminalh|pacia1716|pacib1716|sha256su0|sha256su1|sha512su0|sha512su1|sm3partw1|sm3partw2|sqdmlalbt|sqdmlslbt|sqrdcmlah|sqrshrun2|sqrshrunb|sqrshrunt|cpyertrn|cpyertwn|cpyewtrn|cpyewtwn|cpyfertn|cpyfetrn|cpyfetwn|cpyfewtn|cpyfmrtn|cpyfmtrn|cpyfmtwn|cpyfmwtn|cpyfprtn|cpyfptrn|cpyfptwn|cpyfpwtn|cpymrtrn|cpymrtwn|cpymwtrn|cpymwtwn|cpyprtrn|cpyprtwn|cpypwtrn|cpypwtwn|frint32x|frint32z|frint64x|frint64z|ldaddalb|ldaddalh|ldapursb|ldapursh|ldapursw|ldclralb|ldclralh|ldeoralb|ldeoralh|ldsetalb|ldsetalh|ldsmaxab|ldsmaxah|ldsmaxal|ldsmaxlb|ldsmaxlh|ldsminab|ldsminah|ldsminal|ldsminlb|ldsminlh|ldumaxab|ldumaxah|ldumaxal|ldumaxlb|ldumaxlh|lduminab|lduminah|lduminal|lduminlb|lduminlh|sha256h2|sha512h2|sqdmlal2|sqdmlalb|sqdmlalt|sqdmlsl2|sqdmlslb|sqdmlslt|sqdmull2|sqdmullb|sqdmullt|sqrdmlah|sqrdmlsh|sqrdmulh|sqrshrn2|sqrshrnb|sqrshrnt|sqrshrun|sqshrun2|sqshrunb|sqshrunt|stsmaxlb|stsmaxlh|stsminlb|stsminlh|stumaxlb|stumaxlh|stuminlb|stuminlh|uqrshrn2|uqrshrnb|uqrshrnt|autiasp|autibsp|bfcvtn2|bfcvtnt|bfmlalb|bfmlalt|compact|cpyertn|cpyetrn|cpyetwn|cpyewtn|cpyfern|cpyfert|cpyfetn|cpyfewn|cpyfewt|cpyfmrn|cpyfmrt|cpyfmtn|cpyfmwn|cpyfmwt|cpyfprn|cpyfprt|cpyfptn|cpyfpwn|cpyfpwt|cpymrtn|cpymtrn|cpymtwn|cpymwtn|cpyprtn|cpyptrn|cpyptwn|cpypwtn|crc32cb|crc32ch|crc32cw|crc32cx|ctermeq|ctermne|fcvtxn2|fcvtxnt|fjcvtzs|fmaxnmp|fmaxnmv|fminnmp|fminnmv|frsqrte|frsqrts|histcnt|histseg|ldaddab|ldaddah|ldaddal|ldaddlb|ldaddlh|ldapurb|ldapurh|ldclrab|ldclrah|ldclral|ldclrlb|ldclrlh|ldeorab|ldeorah|ldeoral|ldeorlb|ldeorlh|ldff1sb|ldff1sh|ldff1sw|ldnf1sb|ldnf1sh|ldnf1sw|ldnt1sb|ldnt1sh|ldnt1sw|ldsetab|ldsetah|ldsetal|ldsetlb|ldsetlh|ldsmaxa|ldsmaxb|ldsmaxh|ldsmaxl|ldsmina|ldsminb|ldsminh|ldsminl|ldumaxa|ldumaxb|ldumaxh|ldumaxl|ldumina|lduminb|lduminh|lduminl|movprfx|paciasp|pacibsp|punpkhi|punpklo|raddhn2|raddhnb|raddhnt|rsubhn2|rsubhnb|rsubhnt|saddlbt|setgetn|setgmtn|setgptn|sha1su0|sha1su1|sha256h|sha512h|sm3tt1a|sm3tt1b|sm3tt2a|sm3tt2b|sm4ekey|smstart|sqdmlal|sqdmlsl|sqdmulh|sqdmull|sqrshlr|sqrshrn|sqshrn2|sqshrnb|sqshrnt|sqshrun|sqxtun2|sqxtunb|sqxtunt|ssublbt|ssubltb|st64bv0|staddlb|staddlh|stclrlb|stclrlh|steorlb|steorlh|stsetlb|stsetlh|stsmaxb|stsmaxh|stsmaxl|stsminb|stsminh|stsminl|stumaxb|stumaxh|stumaxl|stuminb|stuminh|stuminl|sunpkhi|sunpklo|tcancel|tcommit|uqrshlr|uqrshrn|uqshrn2|uqshrnb|uqshrnt|ursqrte|uunpkhi|uunpklo|whilege|whilegt|whilehi|whilehs|whilele|whilelo|whilels|whilelt|whilerw|whilewr|xpaclri|addhn2|addhnb|addhnt|aesimc|autdza|autdzb|autiaz|autibz|autiza|autizb|axflag|bfcvtn|bfmmla|bfmopa|bfmops|blraaz|blrabz|brkpas|brkpbs|casalb|casalh|caspal|clasta|clastb|cpyern|cpyert|cpyetn|cpyewn|cpyewt|cpyfen|cpyfet|cpyfmn|cpyfmt|cpyfpn|cpyfpt|cpymrn|cpymrt|cpymtn|cpymwn|cpymwt|cpyprn|cpyprt|cpyptn|cpypwn|cpypwt|crc32b|crc32h|crc32w|crc32x|eretaa|eretab|fccmpe|fcvtas|fcvtau|fcvtl2|fcvtlt|fcvtms|fcvtmu|fcvtn2|fcvtns|fcvtnt|fcvtnu|fcvtps|fcvtpu|fcvtxn|fcvtzs|fcvtzu|fmaxnm|fminnm|fmlal2|fmlalb|fmlalt|fmlsl2|fmlslb|fmlslt|fnmadd|fnmsub|frecpe|frecps|frecpx|frinta|frinti|frintm|frintn|frintp|frintx|frintz|fscale|ftsmul|ftssel|ld1rob|ld1rod|ld1roh|ld1row|ld1rqb|ld1rqd|ld1rqh|ld1rqw|ld1rsb|ld1rsh|ld1rsw|ldadda|ldaddb|ldaddh|ldaddl|ldaprb|ldaprh|ldapur|ldaxrb|ldaxrh|ldclra|ldclrb|ldclrh|ldclrl|ldeora|ldeorb|ldeorh|ldeorl|ldff1b|ldff1d|ldff1h|ldff1w|ldlarb|ldlarh|ldnf1b|ldnf1d|ldnf1h|ldnf1w|ldnt1b|ldnt1d|ldnt1h|ldnt1w|ldseta|ldsetb|ldseth|ldsetl|ldsmax|ldsmin|ldtrsb|ldtrsh|ldtrsw|ldumax|ldumin|ldursb|ldursh|ldursw|nmatch|pacdza|pacdzb|paciaz|pacibz|paciza|pacizb|pfalse|pfirst|pmull2|pmullb|pmullt|ptrues|raddhn|rdffrs|rshrn2|rshrnb|rshrnt|rsubhn|sabal2|sabalb|sabalt|sabdl2|sabdlb|sabdlt|sadalp|saddl2|saddlb|saddlp|saddlt|saddlv|saddw2|saddwb|saddwt|sclamp|setetn|setf16|setffr|setgen|setget|setgmn|setgmt|setgpn|setgpt|setmtn|setptn|shsubr|sm3ss1|smaddl|smlal2|smlalb|smlalt|smlsl2|smlslb|smlslt|smnegl|smstop|smsubl|smull2|smullb|smullt|splice|sqcadd|sqdecb|sqdecd|sqdech|sqdecp|sqdecw|sqincb|sqincd|sqinch|sqincp|sqincw|sqrshl|sqshlr|sqshlu|sqshrn|sqsubr|sqxtn2|sqxtnb|sqxtnt|sqxtun|srhadd|srshlr|sshll2|sshllb|sshllt|ssubl2|ssublb|ssublt|ssubw2|ssubwb|ssubwt|st64bv|staddb|staddh|staddl|stclrb|stclrh|stclrl|steorb|steorh|steorl|stllrb|stllrh|stlurb|stlurh|stlxrb|stlxrh|stnt1b|stnt1d|stnt1h|stnt1w|stsetb|stseth|stsetl|stsmax|stsmin|stumax|stumin|subhn2|subhnb|subhnt|sumopa|sumops|suqadd|swpalb|swpalh|tstart|uabal2|uabalb|uabalt|uabdl2|uabdlb|uabdlt|uadalp|uaddl2|uaddlb|uaddlp|uaddlt|uaddlv|uaddw2|uaddwb|uaddwt|uclamp|uhsubr|umaddl|umlal2|umlalb|umlalt|umlsl2|umlslb|umlslt|umnegl|umsubl|umull2|umullb|umullt|uqdecb|uqdecd|uqdech|uqdecp|uqdecw|uqincb|uqincd|uqinch|uqincp|uqincw|uqrshl|uqshlr|uqshrn|uqsubr|uqxtn2|uqxtnb|uqxtnt|urecpe|urhadd|urshlr|ushll2|ushllb|ushllt|usmmla|usmopa|usmops|usqadd|usubl2|usublb|usublt|usubw2|usubwb|usubwt|xaflag|adclb|adclt|addha|addhn|addpl|addva|addvl|aesmc|autda|autdb|autia|autib|bfcvt|bfdot|bfxil|blraa|blrab|braaz|brabz|brkas|brkbs|brkns|brkpa|brkpb|bsl1n|bsl2n|casab|casah|casal|caslb|caslh|caspa|caspl|cfinv|clrex|cmpeq|cmpge|cmpgt|cmphi|cmphs|cmple|cmplo|cmpls|cmplt|cmpne|cmtst|cpyen|cpyet|cpyfe|cpyfm|cpyfp|cpymn|cpymt|cpypn|cpypt|csetm|csinc|csinv|csneg|dcps1|dcps2|dcps3|eorbt|eortb|facge|facgt|facle|faclt|fadda|faddp|faddv|fcadd|fccmp|fcmeq|fcmge|fcmgt|fcmla|fcmle|fcmlt|fcmne|fcmpe|fcmuo|fcsel|fcvtl|fcvtn|fcvtx|fdivr|fexpa|flogb|fmadd|fmaxp|fmaxv|fminp|fminv|fmlal|fmlsl|fmmla|fmopa|fmops|fmsub|fmulx|fnmad|fnmla|fnmls|fnmsb|fnmul|fsqrt|fsubr|ftmad|index|lasta|lastb|ld1rb|ld1rd|ld1rh|ld1rw|ld1sb|ld1sh|ld1sw|ld64b|ldadd|ldapr|ldarb|ldarh|ldaxp|ldaxr|ldclr|ldeor|ldlar|ldpsw|ldraa|ldrab|ldrsb|ldrsh|ldrsw|ldset|ldtrb|ldtrh|ldurb|ldurh|ldxrb|ldxrh|match|nands|pacda|pacdb|pacga|pacia|pacib|pmull|pnext|prfum|pssbb|ptest|ptrue|rdffr|retaa|retab|rev16|rev32|rev64|rshrn|sabal|sabdl|saddl|saddv|saddw|sbclb|sbclt|sbfiz|scvtf|sdivr|seten|setet|setf8|setge|setgm|setgp|setmn|setmt|setpn|setpt|sha1c|sha1h|sha1m|sha1p|shadd|shll2|shrn2|shrnb|shrnt|shsub|smaxp|smaxv|sminp|sminv|smlal|smlsl|smmla|smopa|smops|smulh|smull|sqabs|sqadd|sqneg|sqshl|sqsub|sqxtn|srshl|srshr|srsra|sshll|ssubl|ssubw|st64b|stadd|stclr|steor|stllr|stlrb|stlrh|stlur|stlxp|stlxr|stset|sttrb|sttrh|sturb|sturh|stxrb|stxrh|stz2g|stzgm|subhn|subps|sudot|swpab|swpah|swpal|swplb|swplh|sxtl2|ttest|uabal|uabdl|uaddl|uaddv|uaddw|ubfiz|ucvtf|udivr|uhadd|uhsub|umaxp|umaxv|uminp|uminv|umlal|umlsl|ummla|umopa|umops|umulh|umull|uqadd|uqshl|uqsub|uqxtn|urshl|urshr|ursra|usdot|ushll|usubl|usubw|uxtl2|wrffr|xpacd|xpaci|yield|adcs|addg|addp|adds|addv|adrp|aesd|aese|ands|andv|asrd|asrr|asrv|bcax|bdep|bext|bgrp|bics|braa|brab|brka|brkb|brkn|cadd|casa|casb|cash|casl|casp|cbnz|ccmn|ccmp|cdot|cinc|cinv|cmeq|cmge|cmgt|cmhi|cmhs|cmla|cmle|cmlo|cmls|cmlt|cmpp|cneg|cnot|cntb|cntd|cnth|cntp|cntw|cpye|cpym|cpyp|csdb|csel|cset|decb|decd|dech|decp|decw|drps|dupm|eor3|eors|eorv|eret|extr|fabd|fabs|fadd|fcmp|fcpy|fcvt|fdiv|fdup|fmad|fmax|fmin|fmla|fmls|fmov|fmsb|fmul|fneg|fsub|hint|incb|incd|inch|incp|incw|insr|ld1b|ld1d|ld1h|ld1q|ld1r|ld1w|ld2b|ld2d|ld2h|ld2r|ld2w|ld3b|ld3d|ld3h|ld3r|ld3w|ld4b|ld4d|ld4h|ld4r|ld4w|ldar|ldgm|ldnp|ldrb|ldrh|ldtr|ldur|ldxp|ldxr|lslr|lslv|lsrr|lsrv|madd|mneg|mova|movi|movk|movn|movs|movz|msub|mvni|nand|nbsl|negs|ngcs|nors|nots|orns|orrs|pmul|prfb|prfd|prfh|prfm|prfw|psel|rax1|rbit|rdvl|revb|revd|revh|revw|rmif|rorv|saba|sabd|sbcs|sbfm|sbfx|sdiv|sdot|sete|setm|setp|sevl|shll|shrn|sm4e|smax|smin|smov|ssbb|sshl|sshr|ssra|st1b|st1d|st1h|st1q|st1w|st2b|st2d|st2g|st2h|st2w|st3b|st3d|st3h|st3w|st4b|st4d|st4h|st4w|stgm|stgp|stlr|stnp|strb|strh|sttr|stur|stxp|stxr|stzg|subg|subp|subr|subs|swpa|swpb|swph|swpl|sxtb|sxth|sxtl|sxtw|sysl|tbnz|tlbi|trn1|trn2|uaba|uabd|ubfm|ubfx|udiv|udot|umax|umin|umov|ushl|ushr|usra|uxtb|uxth|uxtl|uxtw|uzp1|uzp2|wfet|wfit|xtn2|zero|zip1|zip2|abs|adc|add|adr|and|asr|bfi|bfm|bic|bif|bit|blr|brb|brk|bsl|bti|cas|cbz|cls|clz|cmn|cmp|cnt|cpy|dfb|dgh|dmb|dsb|dup|eon|eor|esb|ext|gmi|hlt|hvc|ins|irg|isb|ld1|ld2|ld3|ld4|ldg|ldp|ldr|lsl|lsr|mad|mla|mls|mov|mrs|msb|msr|mul|mvn|neg|ngc|nop|nor|not|orn|orr|orv|psb|ret|rev|ror|sbc|sel|sev|shl|sli|smc|sri|st1|st2|st3|st4|stg|stp|str|sub|svc|swp|sys|tbl|tbx|tbz|tsb|tst|udf|wfe|wfi|xar|xtn|at|bc|bl|br|dc|ic|sb|b)s?'
ARM64_REGISTERS = '(?:v10|v11|v12|v13|v14|v15|v16|v17|v18|v19|v20|v21|v22|v23|v24|v25|v26|v27|v28|v29|v30|v31|z10|z11|z12|z13|z14|z15|z16|z17|z18|z19|z20|z21|z22|z23|z24|z25|z26|z27|z28|z29|z30|z31|v0|v1|v2|v3|v4|v5|v6|v7|v8|v9|z0|z1|z2|z3|z4|z5|z6|z7|z8|z9)(?:\\.(?:16b|8b|8h|4h|4s|2s|2d|1d|1q|b|h|s|d))?|zaq10|zaq11|zaq12|zaq13|zaq14|zaq15|nzcv|zab0|zad0|zad1|zad2|zad3|zad4|zad5|zad6|zad7|zah0|zah1|zaq0|zaq1|zaq2|zaq3|zaq4|zaq5|zaq6|zaq7|zaq8|zaq9|zas0|zas1|zas2|zas3|b10|b11|b12|b13|b14|b15|b16|b17|b18|b19|b20|b21|b22|b23|b24|b25|b26|b27|b28|b29|b30|b31|d10|d11|d12|d13|d14|d15|d16|d17|d18|d19|d20|d21|d22|d23|d24|d25|d26|d27|d28|d29|d30|d31|ffr|h10|h11|h12|h13|h14|h15|h16|h17|h18|h19|h20|h21|h22|h23|h24|h25|h26|h27|h28|h29|h30|h31|ip0|ip1|p10|p11|p12|p13|p14|p15|q10|q11|q12|q13|q14|q15|q16|q17|q18|q19|q20|q21|q22|q23|q24|q25|q26|q27|q28|q29|q30|q31|s10|s11|s12|s13|s14|s15|s16|s17|s18|s19|s20|s21|s22|s23|s24|s25|s26|s27|s28|s29|s30|s31|w10|w11|w12|w13|w14|w15|w16|w17|w18|w19|w20|w21|w22|w23|w24|w25|w26|w27|w28|w29|w30|wsp|wzr|x10|x11|x12|x13|x14|x15|x16|x17|x18|x19|x20|x21|x22|x23|x24|x25|x26|x27|x28|x29|x30|xzr|b0|b1|b2|b3|b4|b5|b6|b7|b8|b9|d0|d1|d2|d3|d4|d5|d6|d7|d8|d9|fp|h0|h1|h2|h3|h4|h5|h6|h7|h8|h9|lr|p0|p1|p2|p3|p4|p5|p6|p7|p8|p9|q0|q1|q2|q3|q4|q5|q6|q7|q8|q9|s0|s1|s2|s3|s4|s5|s6|s7|s8|s9|sp|vg|w0|w1|w2|w3|w4|w5|w6|w7|w8|w9|x0|x1|x2|x3|x4|x5|x6|x7|x8|x9|za'
ARM64_OPERAND_KEYWORDS = 'sxtb|sxth|sxtw|sxtx|uxtb|uxth|uxtw|uxtx|asr|lsl|lsr|msl|ror|al|cc|cs|eq|ge|gt|hi|hs|le|lo|ls|lt|mi|ne|nv|pl|vc|vs'
ARM32_MNEMONICS = 'it[te]{0,3}|(?:sha256su0|sha256su1|sha256h2|vqrdmlah|vqrdmlsh|vqrdmulh|vqrshrun|crc32cb|crc32ch|crc32cw|fconstd|fconsts|fldmdbx|fldmiax|fstmdbx|fstmiax|sha1su0|sha1su1|sha256h|shadd16|shsub16|smlalbb|smlalbt|smlaldx|smlaltb|smlaltt|smlsldx|sxtab16|uhadd16|uhsub16|uqadd16|uqsub16|uxtab16|vqdmlal|vqdmlsl|vqdmulh|vqdmull|vqmovun|vqrshrn|vqshrun|vraddhn|vrsqrte|vrsqrts|vrsubhn|aesimc|crc32b|crc32h|crc32w|fcmpzd|fcmpzs|fmstat|ldaexb|ldaexd|ldaexh|ldrexb|ldrexd|ldrexh|ldrsbt|ldrsht|qadd16|qsub16|sadd16|setend|setpan|shadd8|shsub8|smlabb|smlabt|smladx|smlald|smlatb|smlatt|smlawb|smlawt|smlsdx|smlsld|smmlar|smmlsr|smmulr|smuadx|smulbb|smulbt|smultb|smultt|smulwb|smulwt|smusdx|ssat16|ssub16|stlexb|stlexd|stlexh|strexb|strexd|strexh|sxtb16|uadd16|uhadd8|uhsub8|uqadd8|uqsub8|usada8|usat16|usub16|uxtb16|vaddhn|vldmdb|vldmia|vmaxnm|vminnm|vpadal|vpaddl|vqmovn|vqrshl|vqshlu|vqshrn|vrecpe|vrecps|vrev16|vrev32|vrev64|vrhadd|vrinta|vrintm|vrintn|vrintp|vrintr|vrintx|vrintz|vrshrn|vseleq|vselge|vselgt|vselvs|vstmdb|vstmia|vsubhn|aesmc|blxns|clrex|dcps1|dcps2|dcps3|faddd|fadds|fmdhr|fmdlr|fsubd|fsubs|ldaex|ldc2l|ldmda|ldmdb|ldmib|ldrbt|ldrex|ldrht|ldrsb|ldrsh|mcrr2|mrrc2|pkhbt|pkhtb|qadd8|qdadd|qdsub|qsub8|rev16|revsh|rfeda|rfedb|rfeia|rfeib|sadd8|sha1c|sha1h|sha1m|sha1p|shasx|shsax|smlad|smlal|smlsd|smmla|smmls|smmul|smuad|smull|smusd|srsda|srsdb|srsia|srsib|ssub8|stc2l|stlex|stmda|stmdb|stmib|strbt|strex|strht|sxtab|sxtah|uadd8|uhasx|uhsax|umaal|umlal|umull|uqasx|uqsax|usad8|usub8|uxtab|uxtah|vabal|vabdl|vacge|vacgt|vacle|vaclt|vaddl|vaddw|vcadd|vcmla|vcmpe|vcvta|vcvtb|vcvtm|vcvtn|vcvtp|vcvtr|vcvtt|vfnma|vfnms|vhadd|vhsub|vjcvt|vlldm|vlstm|vmlal|vmlsl|vmovl|vmovn|vmovx|vmull|vnmla|vnmls|vnmul|vpadd|vpmax|vpmin|vpush|vqabs|vqadd|vqneg|vqshl|vqsub|vrshl|vrshr|vrsra|vsdot|vshll|vshrn|vsqrt|vsubl|vsubw|vudot|yield|addw|aesd|aese|bkpt|bxns|cbnz|cdp2|csdb|eret|hint|ldab|ldah|ldc2|ldcl|ldrb|ldrd|ldrh|ldrt|mcr2|mcrr|movs|movt|movw|mrc2|mrrc|pldw|push|qadd|qasx|qsax|qsub|rbit|sasx|sbfx|sdiv|sevl|ssat|ssax|stc2|stcl|stlb|stlh|strb|strd|strh|strt|subs|subw|swpb|sxtb|sxth|trap|ttat|uasx|ubfx|udiv|usat|usax|uxtb|uxth|vaba|vabd|vabs|vadd|vand|vbic|vbif|vbit|vbsl|vceq|vcge|vcgt|vcle|vcls|vclt|vclz|vcmp|vcnt|vcvt|vdiv|vdup|veor|vext|vfma|vfms|vins|vld1|vld2|vld3|vld4|vldr|vmax|vmin|vmla|vmls|vmov|vmrs|vmsr|vmul|vmvn|vneg|vorn|vorr|vpop|vshl|vshr|vsli|vsra|vsri|vst1|vst2|vst3|vst4|vstr|vsub|vswp|vtbl|vtbx|vtrn|vtst|vuzp|vzip|adc|add|adr|and|asr|bfc|bfi|bic|blx|bxj|cbz|cdp|clz|cmn|cmp|cps|dbg|dfb|dmb|dsb|eor|esb|hlt|hvc|isb|lda|ldc|ldm|ldr|lsl|lsr|mcr|mla|mls|mov|mrc|mrs|msr|mul|mvn|neg|nop|orn|orr|pld|pli|pop|rev|ror|rrx|rsb|rsc|sbc|sel|sev|smc|stc|stl|stm|str|sub|svc|swp|tbb|tbh|teq|tsb|tst|tta|ttt|udf|wfe|wfi|bl|bx|it|sg|tt|b)s?(?:al|cc|cs|eq|ge|gt|hi|hs|le|lo|ls|lt|mi|ne|pl|vc|vs)?(?:\\.[wn])?'
ARM32_REGISTERS = 'fpscr_nzcv|apsr_nzcv|fpinst2|itstate|fpinst|fpexc|fpscr|fpsid|mvfr0|mvfr1|mvfr2|apsr|cpsr|spsr|d10|d11|d12|d13|d14|d15|d16|d17|d18|d19|d20|d21|d22|d23|d24|d25|d26|d27|d28|d29|d30|d31|q10|q11|q12|q13|q14|q15|r10|r11|r12|r13|r14|r15|s10|s11|s12|s13|s14|s15|s16|s17|s18|s19|s20|s21|s22|s23|s24|s25|s26|s27|s28|s29|s30|s31|d0|d1|d2|d3|d4|d5|d6|d7|d8|d9|fp|ip|lr|pc|q0|q1|q2|q3|q4|q5|q6|q7|q8|q9|r0|r1|r2|r3|r4|r5|r6|r7|r8|r9|s0|s1|s2|s3|s4|s5|s6|s7|s8|s9|sb|sl|sp'
ARM32_OPERAND_KEYWORDS = 'asr|lsl|lsr|ror|rrx|al|cc|cs|eq|ge|gt|hi|hs|le|lo|ls|lt|mi|ne|pl|vc|vs'
X64_MNEMONICS = 'vgf2p8affineinvqb|gf2p8affineinvqb|vaeskeygenassist|aeskeygenassist|vbroadcastf32x2|vbroadcastf32x4|vbroadcastf32x8|vbroadcastf64x2|vbroadcastf64x4|vbroadcasti32x2|vbroadcasti32x4|vbroadcasti32x8|vbroadcasti64x2|vbroadcasti64x4|vpbroadcastmb2q|vpbroadcastmw2d|vbroadcastf128|vbroadcasti128|vfmaddsub132pd|vfmaddsub132ps|vfmaddsub213pd|vfmaddsub213ps|vfmaddsub231pd|vfmaddsub231ps|vfmsubadd132pd|vfmsubadd132ps|vfmsubadd213pd|vfmsubadd213ps|vfmsubadd231pd|vfmsubadd231ps|vgf2p8affineqb|vpmultishiftqb|vscatterpf0dpd|vscatterpf0dps|vscatterpf0qpd|vscatterpf0qps|vscatterpf1dpd|vscatterpf1dps|vscatterpf1qpd|vscatterpf1qps|fdisi8087_nop|gf2p8affineqb|vextractf32x4|vextractf32x8|vextractf64x2|vextractf64x4|vextracti32x4|vextracti32x8|vextracti64x2|vextracti64x4|vgatherpf0dpd|vgatherpf0dps|vgatherpf0qpd|vgatherpf0qps|vgatherpf1dpd|vgatherpf1dps|vgatherpf1qpd|vgatherpf1qps|feni8087_nop|vbroadcastsd|vbroadcastss|vextractf128|vextracti128|vfnmadd132pd|vfnmadd132ps|vfnmadd132sd|vfnmadd132ss|vfnmadd213pd|vfnmadd213ps|vfnmadd213sd|vfnmadd213ss|vfnmadd231pd|vfnmadd231ps|vfnmadd231sd|vfnmadd231ss|vfnmsub132pd|vfnmsub132ps|vfnmsub132sd|vfnmsub132ss|vfnmsub213pd|vfnmsub213ps|vfnmsub213sd|vfnmsub213ss|vfnmsub231pd|vfnmsub231ps|vfnmsub231sd|vfnmsub231ss|vinsertf32x4|vinsertf32x8|vinsertf64x2|vinsertf64x4|vinserti32x4|vinserti32x8|vinserti64x2|vinserti64x4|vpbroadcastb|vpbroadcastd|vpbroadcastq|vpbroadcastw|vpshufbitqmb|prefetchnta|prefetchwt1|saveprevssp|sha256rnds2|vaesdeclast|vaesenclast|vcompresspd|vcompressps|vcvttpd2udq|vcvttpd2uqq|vcvttps2udq|vcvttps2uqq|vcvttsd2usi|vcvttss2usi|vfixupimmpd|vfixupimmps|vfixupimmsd|vfixupimmss|vfmadd132pd|vfmadd132ps|vfmadd132sd|vfmadd132ss|vfmadd213pd|vfmadd213ps|vfmadd213sd|vfmadd213ss|vfmadd231pd|vfmadd231ps|vfmadd231sd|vfmadd231ss|vfmaddsubpd|vfmaddsubps|vfmsub132pd|vfmsub132ps|vfmsub132sd|vfmsub132ss|vfmsub213pd|vfmsub213ps|vfmsub213sd|vfmsub213ss|vfmsub231pd|vfmsub231ps|vfmsub231sd|vfmsub231ss|vfmsubaddpd|vfmsubaddps|vinsertf128|vinserti128|vmaskmovdqu|vpcompressb|vpcompressd|vpcompressq|vpcompressw|vpconflictd|vpconflictq|vphminposuw|vpmadd52huq|vpmadd52luq|vpscatterdd|vpscatterdq|vpscatterqd|vpscatterqq|vpunpckhqdq|vpunpcklqdq|vrndscalepd|vrndscaleps|vrndscalesd|vrndscaless|vscatterdpd|vscatterdps|vscatterqpd|vscatterqps|aesdeclast|aesenclast|clflushopt|cmpxchg16b|maskmovdqu|phminposuw|prefetcht0|prefetcht1|prefetcht2|punpckhqdq|punpcklqdq|sha256msg1|sha256msg2|v4fnmaddps|v4fnmaddss|vcvtpd2udq|vcvtpd2uqq|vcvtps2udq|vcvtps2uqq|vcvtsd2usi|vcvtss2usi|vcvttpd2dq|vcvttpd2qq|vcvttps2dq|vcvttps2qq|vcvttsd2si|vcvttss2si|vcvtudq2pd|vcvtudq2ps|vcvtuqq2pd|vcvtuqq2ps|vcvtusi2sd|vcvtusi2ss|vextractps|vfpclasspd|vfpclassps|vfpclasssd|vfpclassss|vgatherdpd|vgatherdps|vgatherqpd|vgatherqps|vgetmantpd|vgetmantps|vgetmantsd|vgetmantss|vgf2p8mulb|vmaskmovpd|vmaskmovps|vp4dpwssds|vpclmulqdq|vpcmpestri|vpcmpestrm|vpcmpistri|vpcmpistrm|vperm2f128|vperm2i128|vpermil2pd|vpermil2ps|vpgatherdd|vpgatherdq|vpgatherqd|vpgatherqq|vpmacssdqh|vpmacssdql|vpmadcsswd|vpmaddubsw|vpmaskmovd|vpmaskmovq|vpternlogd|vpternlogq|vpunpckhbw|vpunpckhdq|vpunpckhwd|vpunpcklbw|vpunpckldq|vpunpcklwd|vrsqrt14pd|vrsqrt14ps|vrsqrt14sd|vrsqrt14ss|vrsqrt28pd|vrsqrt28ps|vrsqrt28sd|vrsqrt28ss|vshuff32x4|vshuff64x2|vshufi32x4|vshufi64x2|vzeroupper|xsaveopt64|cmpxchg8b|cvttpd2dq|cvttpd2pi|cvttps2dq|cvttps2pi|cvttsd2si|cvttss2si|extractps|fxrstor64|gf2p8mulb|movdir64b|pclmulqdq|pcmpestri|pcmpestrm|pcmpistri|pcmpistrm|pmaddubsw|prefetchw|punpckhbw|punpckhdq|punpckhwd|punpcklbw|punpckldq|punpcklwd|sha1nexte|sha1rnds4|v4fmaddps|v4fmaddss|vaddsubpd|vaddsubps|vblendmpd|vblendmps|vblendvpd|vblendvps|vcvtdq2pd|vcvtdq2ps|vcvtpd2dq|vcvtpd2ps|vcvtpd2qq|vcvtph2ps|vcvtps2dq|vcvtps2pd|vcvtps2ph|vcvtps2qq|vcvtqq2pd|vcvtqq2ps|vcvtsd2si|vcvtsd2ss|vcvtsi2sd|vcvtsi2ss|vcvtss2sd|vcvtss2si|vdbpsadbw|vexpandpd|vexpandps|vfnmaddpd|vfnmaddps|vfnmaddsd|vfnmaddss|vfnmsubpd|vfnmsubps|vfnmsubsd|vfnmsubss|vgetexppd|vgetexpps|vgetexpsd|vgetexpss|vinsertps|vmovdqa32|vmovdqa64|vmovdqu16|vmovdqu32|vmovdqu64|vmovmskpd|vmovmskps|vmovntdqa|vmovshdup|vmovsldup|vp4dpwssd|vpackssdw|vpacksswb|vpackusdw|vpackuswb|vpblendmb|vpblendmd|vpblendmq|vpblendmw|vpblendvb|vpdpbusds|vpdpwssds|vpermi2pd|vpermi2ps|vpermilpd|vpermilps|vpermt2pd|vpermt2ps|vpexpandb|vpexpandd|vpexpandq|vpexpandw|vphaddubd|vphaddubq|vphaddubw|vphaddudq|vphadduwd|vphadduwq|vpmacsdqh|vpmacsdql|vpmacssdd|vpmacsswd|vpmacssww|vpmadcswd|vpmovmskb|vpmovsxbd|vpmovsxbq|vpmovsxbw|vpmovsxdq|vpmovsxwd|vpmovsxwq|vpmovusdb|vpmovusdw|vpmovusqb|vpmovusqd|vpmovusqw|vpmovuswb|vpmovzxbd|vpmovzxbq|vpmovzxbw|vpmovzxdq|vpmovzxwd|vpmovzxwq|vpmulhrsw|vptestnmb|vptestnmd|vptestnmq|vptestnmw|vreducepd|vreduceps|vreducesd|vreducess|vscalefpd|vscalefps|vscalefsd|vscalefss|vunpckhpd|vunpckhps|vunpcklpd|vunpcklps|xcryptcbc|xcryptcfb|xcryptctr|xcryptecb|xcryptofb|xrstors64|addsubpd|addsubps|blendvpd|blendvps|cldemote|clrssbsy|cvtdq2pd|cvtdq2ps|cvtpd2dq|cvtpd2pi|cvtpd2ps|cvtpi2pd|cvtpi2ps|cvtps2dq|cvtps2pd|cvtps2pi|cvtsd2si|cvtsd2ss|cvtsi2sd|cvtsi2ss|cvtss2sd|cvtss2si|fcmovnbe|fxsave64|insertps|kortestb|kortestd|kortestq|kortestw|kshiftlb|kshiftld|kshiftlq|kshiftlw|kshiftrb|kshiftrd|kshiftrq|kshiftrw|kunpckbw|kunpckdq|kunpckwd|maskmovq|monitorx|movmskpd|movmskps|movntdqa|movshdup|movsldup|packssdw|packsswb|packusdw|packuswb|pblendvb|pfrcpit1|pfrcpit2|pfrsqit1|pmovmskb|pmovsxbd|pmovsxbq|pmovsxbw|pmovsxdq|pmovsxwd|pmovsxwq|pmovzxbd|pmovzxbq|pmovzxbw|pmovzxdq|pmovzxwd|pmovzxwq|pmulhrsw|prefetch|rdfsbase|rdgsbase|rstorssp|setssbsy|sha1msg1|sha1msg2|sysenter|sysexitq|umonitor|unpckhpd|unpckhps|unpcklpd|unpcklps|vblendpd|vblendps|vfmaddpd|vfmaddps|vfmaddsd|vfmaddss|vfmsubpd|vfmsubps|vfmsubsd|vfmsubss|vldmxcsr|vmlaunch|vmovddup|vmovdqu8|vmovhlps|vmovlhps|vmovntdq|vmovntpd|vmovntps|vmpsadbw|vmresume|vpaddusb|vpaddusw|vpalignr|vpblendd|vpblendw|vpcmpeqb|vpcmpeqd|vpcmpeqq|vpcmpeqw|vpcmpgtb|vpcmpgtd|vpcmpgtq|vpcmpgtw|vpdpbusd|vpdpwssd|vpermi2b|vpermi2d|vpermi2q|vpermi2w|vpermt2b|vpermt2d|vpermt2q|vpermt2w|vphaddbd|vphaddbq|vphaddbw|vphadddq|vphaddsw|vphaddwd|vphaddwq|vphsubbw|vphsubdq|vphsubsw|vphsubwd|vplzcntd|vplzcntq|vpmacsdd|vpmacswd|vpmacsww|vpmaddwd|vpmovb2m|vpmovd2m|vpmovm2b|vpmovm2d|vpmovm2q|vpmovm2w|vpmovq2m|vpmovsdb|vpmovsdw|vpmovsqb|vpmovsqd|vpmovsqw|vpmovswb|vpmovw2m|vpmulhuw|vpmuludq|vpopcntb|vpopcntd|vpopcntq|vpopcntw|vpshldvd|vpshldvq|vpshldvw|vpshrdvd|vpshrdvq|vpshrdvw|vpshufhw|vpshuflw|vpsubusb|vpsubusw|vptestmb|vptestmd|vptestmq|vptestmw|vrangepd|vrangeps|vrangesd|vrangess|vrcp14pd|vrcp14ps|vrcp14sd|vrcp14ss|vrcp28pd|vrcp28ps|vrcp28sd|vrcp28ss|vroundpd|vroundps|vroundsd|vroundss|vrsqrtps|vrsqrtss|vstmxcsr|vucomisd|vucomiss|vzeroall|wbnoinvd|wrfsbase|wrgsbase|xacquire|xrelease|xrstor64|xsavec64|xsaveopt|xsaves64|blcfill|blendpd|blendps|blsfill|clflush|cmpxchg|endbr32|endbr64|fcmovbe|fcmovnb|fcmovne|fcmovnp|fcmovnu|fdecstp|fincstp|fnstenv|frndint|fsincos|fstpnce|fucompi|fucompp|fxrstor|fxtract|fyl2xp1|incsspd|incsspq|insertq|invlpga|invpcid|invvpid|ldmxcsr|monitor|montmul|movddup|movdiri|movdq2q|movhlps|movlhps|movntdq|movntpd|movntps|movntsd|movntss|movq2dq|mpsadbw|notrack|paddusb|paddusw|palignr|pavgusb|pblendw|pcmpeqb|pcmpeqd|pcmpeqq|pcmpeqw|pcmpgtb|pcmpgtd|pcmpgtq|pcmpgtw|pconfig|pfcmpeq|pfcmpge|pfcmpgt|pfpnacc|pfrsqrt|phaddsw|phsubsw|pmaddwd|pmulhrw|pmulhuw|pmuludq|pshufhw|pshuflw|psubusb|psubusw|ptwrite|roundpd|roundps|roundsd|roundss|rsqrtps|rsqrtss|stmxcsr|syscall|sysexit|sysretq|ucomisd|ucomiss|vaesdec|vaesenc|vaesimc|valignd|valignq|vandnpd|vandnps|vcomisd|vcomiss|vexp2pd|vexp2ps|vfrczpd|vfrczps|vfrczsd|vfrczss|vhaddpd|vhaddps|vhsubpd|vhsubps|vmclear|vmmcall|vmovapd|vmovaps|vmovdqa|vmovdqu|vmovhpd|vmovhps|vmovlpd|vmovlps|vmovupd|vmovups|vmptrld|vmptrst|vmwrite|vpaddsb|vpaddsw|vpandnd|vpandnq|vpcmpub|vpcmpud|vpcmpuq|vpcmpuw|vpcomub|vpcomud|vpcomuq|vpcomuw|vpermpd|vpermps|vpextrb|vpextrd|vpextrq|vpextrw|vphaddd|vphaddw|vphsubd|vphsubw|vpinsrb|vpinsrd|vpinsrq|vpinsrw|vpmaxsb|vpmaxsd|vpmaxsq|vpmaxsw|vpmaxub|vpmaxud|vpmaxuq|vpmaxuw|vpminsb|vpminsd|vpminsq|vpminsw|vpminub|vpminud|vpminuq|vpminuw|vpmovdb|vpmovdw|vpmovqb|vpmovqd|vpmovqw|vpmovwb|vpmuldq|vpmulhw|vpmulld|vpmullq|vpmullw|vprolvd|vprolvq|vprorvd|vprorvq|vpsadbw|vpshldd|vpshldq|vpshldw|vpshrdd|vpshrdq|vpshrdw|vpshufb|vpshufd|vpsignb|vpsignd|vpsignw|vpslldq|vpsllvd|vpsllvq|vpsllvw|vpsravd|vpsravq|vpsravw|vpsrldq|vpsrlvd|vpsrlvq|vpsrlvw|vpsubsb|vpsubsw|vshufpd|vshufps|vsqrtpd|vsqrtps|vsqrtsd|vsqrtss|vtestpd|vtestps|xrstors|xsave64|xsha256|aesdec|aesenc|aesimc|andnpd|andnps|blcmsk|blsmsk|bndldx|bndmov|bndstx|clzero|cmovae|cmovbe|cmovge|cmovle|cmovne|cmovno|cmovnp|cmovns|comisd|comiss|data16|fcmovb|fcmove|fcmovu|fcompi|fcompp|fdivrp|ffreep|ficomp|fidivr|fisttp|fisubr|fldenv|fldl2e|fldl2t|fldlg2|fldln2|fnclex|fninit|fnsave|fnstcw|fnstsw|fpatan|fprem1|frstor|fscale|fsetpm|fsubrp|fucomi|fucomp|fxsave|getsec|haddpd|haddps|hsubpd|hsubps|invept|invlpg|kandnb|kandnd|kandnq|kandnw|ktestb|ktestd|ktestq|ktestw|kxnorb|kxnord|kxnorq|kxnorw|lfence|llwpcb|loopne|lwpins|lwpval|mfence|movabs|movapd|movaps|movdqa|movdqu|movhpd|movhps|movlpd|movlps|movnti|movntq|movsxd|movupd|movups|mwaitx|paddsb|paddsw|pextrb|pextrd|pextrq|pextrw|pfnacc|pfsubr|phaddd|phaddw|phsubd|phsubw|pinsrb|pinsrd|pinsrq|pinsrw|pmaxsb|pmaxsd|pmaxsw|pmaxub|pmaxud|pmaxuw|pminsb|pminsd|pminsw|pminub|pminud|pminuw|pmuldq|pmulhw|pmulld|pmullw|popcnt|psadbw|pshufb|pshufd|pshufw|psignb|psignd|psignw|pslldq|psrldq|psubsb|psubsw|pswapd|pushal|pushaw|pushfd|pushfq|rdpkru|rdrand|rdseed|rdsspd|rdsspq|rdtscp|sfence|shufpd|shufps|skinit|slwpcb|sqrtpd|sqrtps|sqrtsd|sqrtss|swapgs|sysret|t1mskc|tpause|umwait|vaddpd|vaddps|vaddsd|vaddss|vandpd|vandps|vcmppd|vcmpps|vcmpsd|vcmpss|vdivpd|vdivps|vdivsd|vdivss|vlddqu|vmaxpd|vmaxps|vmaxsd|vmaxss|vmcall|vmfunc|vminpd|vminps|vminsd|vminss|vmload|vmovsd|vmovss|vmread|vmsave|vmulpd|vmulps|vmulsd|vmulss|vmxoff|vpabsb|vpabsd|vpabsq|vpabsw|vpaddb|vpaddd|vpaddq|vpaddw|vpandd|vpandn|vpandq|vpavgb|vpavgw|vpcmov|vpcmpb|vpcmpd|vpcmpq|vpcmpw|vpcomb|vpcomd|vpcomq|vpcomw|vpermb|vpermd|vpermq|vpermw|vpperm|vprold|vprolq|vprord|vprorq|vprotb|vprotd|vprotq|vprotw|vpshab|vpshad|vpshaq|vpshaw|vpshlb|vpshld|vpshlq|vpshlw|vpslld|vpsllq|vpsllw|vpsrad|vpsraq|vpsraw|vpsrld|vpsrlq|vpsrlw|vpsubb|vpsubd|vpsubq|vpsubw|vptest|vpxord|vpxorq|vrcpps|vrcpss|vsubpd|vsubps|vsubsd|vsubss|vxorpd|vxorps|wbinvd|wrpkru|wrussd|wrussq|xabort|xbegin|xgetbv|xrstor|xsavec|xsaves|xsetbv|xstore|addpd|addps|addsd|addss|andpd|andps|bextr|blcic|blsic|bndcl|bndcn|bndcu|bndmk|bound|bswap|cmova|cmovb|cmove|cmovg|cmovl|cmovo|cmovp|cmovs|cmppd|cmpps|cmpsb|cmpsd|cmpsq|cmpss|cmpsw|cpuid|crc32|divpd|divps|divsd|divss|encls|enclu|enclv|enter|extrq|f2xm1|fbstp|fcomi|fcomp|fdivp|fdivr|femms|ffree|fiadd|ficom|fidiv|fimul|fistp|fisub|fldcw|fldpi|fmulp|fprem|fptan|fsqrt|fsubp|fsubr|fucom|fyl2x|iretd|iretq|jecxz|jrcxz|kaddb|kaddd|kaddq|kaddw|kandb|kandd|kandq|kandw|kmovb|kmovd|kmovq|kmovw|knotb|knotd|knotq|knotw|kxorb|kxord|kxorq|kxorw|lcall|lddqu|leave|lodsb|lodsd|lodsq|lodsw|loope|lzcnt|maxpd|maxps|maxsd|maxss|minpd|minps|minsd|minss|movbe|movsb|movsd|movsq|movss|movsw|movsx|movzx|mulpd|mulps|mulsd|mulss|mwait|outsb|outsd|outsw|pabsb|pabsd|pabsw|paddb|paddd|paddq|paddw|pandn|pause|pavgb|pavgw|pf2id|pf2iw|pfacc|pfadd|pfmax|pfmin|pfmul|pfrcp|pfsub|pi2fd|pi2fw|popal|popaw|popfd|popfq|pslld|psllq|psllw|psrad|psraw|psrld|psrlq|psrlw|psubb|psubd|psubq|psubw|ptest|pushf|rcpps|rcpss|rdmsr|rdpid|rdpmc|rdtsc|repne|repnz|retfq|rex64|scasb|scasd|scasq|scasw|setae|setbe|setge|setle|setne|setno|setnp|setns|stosb|stosd|stosq|stosw|subpd|subps|subsd|subss|tzcnt|tzmsk|vdppd|vdpps|vmovd|vmovq|vmrun|vmxon|vorpd|vorps|vpand|vpcmp|vpcom|vpord|vporq|vpxor|wrmsr|wrssd|wrssq|xlatb|xorpd|xorps|xsave|xsha1|xtest|adcx|adox|andn|arpl|blci|blcs|blsi|blsr|bzhi|call|cdqe|clac|clgi|clts|clwb|cwde|dppd|dpps|emms|fabs|fadd|fbld|fchs|fcom|fcos|fdiv|fild|fist|fld1|fldz|fmul|fnop|fsin|fstp|fsub|ftst|fxam|fxch|idiv|imul|insb|insd|insw|int1|int3|into|invd|iret|jcxz|korb|kord|korq|korw|lahf|lgdt|lidt|ljmp|lldt|lmsw|lock|loop|movd|movq|mulx|orpd|orps|pand|pdep|pext|popf|push|pxor|repe|repz|retf|rorx|sahf|salc|sarx|seta|setb|sete|setg|setl|seto|setp|sets|sgdt|shld|shlx|shrd|shrx|sidt|sldt|smsw|stac|stgi|test|vcmp|verr|verw|vpor|wait|xadd|xchg|xend|aaa|aad|aam|aas|adc|add|and|bsf|bsr|btc|btr|bts|cbw|cdq|clc|cld|cli|cmc|cmp|cqo|cwd|daa|das|dec|div|fld|fst|hlt|inc|int|jae|jbe|jge|jle|jmp|jne|jno|jnp|jns|lar|lds|lea|les|lfs|lgs|lsl|lss|ltr|mov|mul|neg|nop|not|out|pop|por|rcl|rcr|rep|ret|rol|ror|rsm|sal|sar|sbb|shl|shr|stc|std|sti|str|sub|ud0|ud1|ud2|xor|bt|in|ja|jb|je|jg|jl|jo|jp|js|or'
X64_REGISTERS = 'eflags|xmm10|xmm11|xmm12|xmm13|xmm14|xmm15|xmm16|xmm17|xmm18|xmm19|xmm20|xmm21|xmm22|xmm23|xmm24|xmm25|xmm26|xmm27|xmm28|xmm29|xmm30|xmm31|ymm10|ymm11|ymm12|ymm13|ymm14|ymm15|ymm16|ymm17|ymm18|ymm19|ymm20|ymm21|ymm22|ymm23|ymm24|ymm25|ymm26|ymm27|ymm28|ymm29|ymm30|ymm31|zmm10|zmm11|zmm12|zmm13|zmm14|zmm15|zmm16|zmm17|zmm18|zmm19|zmm20|zmm21|zmm22|zmm23|zmm24|zmm25|zmm26|zmm27|zmm28|zmm29|zmm30|zmm31|bnd0|bnd1|bnd2|bnd3|cr10|cr11|cr12|cr13|cr14|cr15|dr10|dr11|dr12|dr13|dr14|dr15|fpsw|r10b|r10d|r10w|r11b|r11d|r11w|r12b|r12d|r12w|r13b|r13d|r13w|r14b|r14d|r14w|r15b|r15d|r15w|xmm0|xmm1|xmm2|xmm3|xmm4|xmm5|xmm6|xmm7|xmm8|xmm9|ymm0|ymm1|ymm2|ymm3|ymm4|ymm5|ymm6|ymm7|ymm8|ymm9|zmm0|zmm1|zmm2|zmm3|zmm4|zmm5|zmm6|zmm7|zmm8|zmm9|bpl|cr0|cr1|cr2|cr3|cr4|cr5|cr6|cr7|cr8|cr9|dil|dr0|dr1|dr2|dr3|dr4|dr5|dr6|dr7|dr8|dr9|eax|ebp|ebx|ecx|edi|edx|eip|eiz|esi|esp|fp0|fp1|fp2|fp3|fp4|fp5|fp6|fp7|mm0|mm1|mm2|mm3|mm4|mm5|mm6|mm7|r10|r11|r12|r13|r14|r15|r8b|r8d|r8w|r9b|r9d|r9w|rax|rbp|rbx|rcx|rdi|rdx|rip|riz|rsi|rsp|sil|spl|st0|st1|st2|st3|st4|st5|st6|st7|ah|al|ax|bh|bl|bp|bx|ch|cl|cs|cx|dh|di|dl|ds|dx|es|fs|gs|ip|k0|k1|k2|k3|k4|k5|k6|k7|r8|r9|si|sp|ss'
X64_OPERAND_KEYWORDS = 'xmmword|ymmword|zmmword|offset|dword|qword|short|tbyte|byte|word|ptr'
# END GENERATED


def _asm_tokens(
    extra_line_comments: list[str],
    mnemonics: str,
    registers: str,
    operand_keywords: str,
    arm_immediates: bool,
) -> dict:
    """Token rules shared by the three dialect lexers.

    A statement's first word is matched against the generated mnemonic list
    (unknown words stay plain); registers, immediates and operand keywords are
    tokenized in operand position; a leftover bare identifier in operand
    position is a symbol reference (branch target).
    """
    line_comments = [(r"//[^\n]*", Comment.Single)]
    line_comments += [(regex, Comment.Single) for regex in extra_line_comments]

    operands = [
        (r"\n", Whitespace, "#pop"),
        (r"[ \t]+", Whitespace),
        *line_comments,
        (r"/\*", Comment.Multiline, "blockcomment"),
        (rf"\b(?:{registers})\b", Keyword.Type),
        (rf"\b(?:{operand_keywords})\b", Keyword),
    ]
    if arm_immediates:
        operands.append((r"#-?(?:0x[0-9a-f]+|0b[01]+|\d+)", Number))
    operands += [
        (r"0x[0-9a-f]+", Number.Hex),
        (r"0b[01]+", Number.Bin),
        (r"\d+", Number.Integer),
        (r"'[^'\n]*'", String.Char),
        (r'"[^"\n]*"', String),
        (r"[!+\-*]", Operator),
        (r"[\[\]{},]", Punctuation),
        (r"[\w.$]+", Name.Function),
        (r".", Text),
    ]

    return {
        "root": [
            (r"\s+", Whitespace),
            *line_comments,
            (r"/\*", Comment.Multiline, "blockcomment"),
            (r"[\w.$]+:", Name.Function),
            (r"\.[a-z_][\w.]*", Keyword.Pseudo, "operands"),
            (rf"(?:{mnemonics})(?=\s|$)", Keyword, "operands"),
            (r"[a-z_][\w.]*", Text, "operands"),
            (r".", Text),
        ],
        "operands": operands,
        "blockcomment": [
            (r"[^*]+", Comment.Multiline),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"\*", Comment.Multiline),
        ],
    }


class _Arm64Lexer(RegexLexer):
    name = "vrdp-asm-arm64"
    flags = re.IGNORECASE
    tokens = _asm_tokens(
        extra_line_comments=[],
        mnemonics=ARM64_MNEMONICS,
        registers=ARM64_REGISTERS,
        operand_keywords=ARM64_OPERAND_KEYWORDS,
        arm_immediates=True,
    )


class _Arm32Lexer(RegexLexer):
    name = "vrdp-asm-arm32"
    flags = re.IGNORECASE
    tokens = _asm_tokens(
        extra_line_comments=[r"@[^\n]*"],
        mnemonics=ARM32_MNEMONICS,
        registers=ARM32_REGISTERS,
        operand_keywords=ARM32_OPERAND_KEYWORDS,
        arm_immediates=True,
    )


class _X64Lexer(RegexLexer):
    name = "vrdp-asm-x64"
    flags = re.IGNORECASE
    tokens = _asm_tokens(
        extra_line_comments=[r"#[^\n]*"],
        mnemonics=X64_MNEMONICS,
        registers=X64_REGISTERS,
        operand_keywords=X64_OPERAND_KEYWORDS,
        arm_immediates=False,
    )


_LEXERS = {
    "arm64": _Arm64Lexer(),
    "arm32": _Arm32Lexer(),
    "x64": _X64Lexer(),
}


@cache
def _get_style(style_name: str) -> type:
    base_style = get_style_by_name(style_name)
    if style_name != "dracula":
        return base_style

    class AsmDraculaStyle(base_style):
        # Align with the ace dracula theme used by the course's editors:
        # numerics purple, strings yellow. (No-ops where the base already
        # matches; child tokens like Number.Hex inherit.)
        styles = {**base_style.styles, Number: "#bd93f9", String: "#f1fa8c"}

    return AsmDraculaStyle


@cache
def _get_formatter(style_name: str) -> HtmlFormatter:
    return HtmlFormatter(
        style=_get_style(style_name),
        noclasses=True,
        nobackground=True,
    )


def prepare(element_html: str, data: pl.QuestionData) -> None:
    element = lxml.html.fragment_fromstring(element_html)
    pl.check_attribs(element, ["language"], ["style-name"])

    language = pl.get_string_attrib(element, "language")
    if language not in _LEXERS:
        raise KeyError(
            f'Unknown language: "{language}". Must be one of {", ".join(_LEXERS)}'
        )

    style_name = pl.get_string_attrib(element, "style-name", STYLE_NAME_DEFAULT)
    if style_name not in STYLE_MAP:
        raise KeyError(
            f'Unknown style name: "{style_name}". Must be one of {", ".join(STYLE_MAP)}'
        )


def render(element_html: str, data: pl.QuestionData) -> str:
    element = lxml.html.fragment_fromstring(element_html)
    language = pl.get_string_attrib(element, "language")
    style_name = pl.get_string_attrib(element, "style-name", STYLE_NAME_DEFAULT)

    # Strip a single leading newline from the code, if present, so that markup
    # starting on the line after <asm-code> doesn't produce a blank first line.
    code = pl.inner_html(element).removeprefix("\r").removeprefix("\n")

    if data["ai_grading"]:
        # Return just the raw code for AI grading.
        return f"<pre><code>\n{code.strip()}\n</code></pre>"

    highlighted = pygments.highlight(
        unescape(code), _LEXERS[language], _get_formatter(style_name)
    )

    html_params = {
        "code": highlighted,
        "background_color": _get_style(style_name).background_color or "transparent",
    }

    with open("asm-code.mustache", encoding="utf-8") as f:
        return chevron.render(f, html_params).strip()
