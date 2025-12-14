"""Python classes for vortaro."""

from __future__ import annotations  # For forward references

import dataclasses
from typing import TypeVar

@dataclasses.dataclass
class Element:
    """Any element."""


T = TypeVar("T", bound=Element)


@dataclasses.dataclass
class TextOnlyElement(Element):
    """An element that contains only text."""

    text: str = ""


@dataclasses.dataclass
class HasContent[T](Element):
    """An element that contains an ordered list of elements."""

    content: list[T] = dataclasses.field(default_factory=list[T])

    def append(self, element: T):
        """Append an element to the content list."""
        self.content.append(element)


@dataclasses.dataclass
class HasTextInContent[T](HasContent[str | T]):
    """An element that contains an ordered list of elements, interspersed with text."""


@dataclasses.dataclass
class HasKap(Element):
    """An element that has a kap (rootword) element."""

    kap: Kap | None = None


# <!-- [%tekst-stiloj] La unuo <dfn>tekst-stiloj</dfn>
# listigas ĉiujn strukturilojn, kiuj donas stilon al tekstoparto,
# ekz. emfazita, citilita, altigita aŭ malaltigita teksto.
# Aliaj elementoj klarigo kaj tildo kaj sencreferenco same povas esti
# multloke, do ankaŭ ili estas listigitaj tie ĉi. -->
# <!-- tekst-stiloj -->
# <!ENTITY % tekst-stiloj "tld|sncref|klr|em|ts|sup|sub|ctl|mis|frm|nom|nac|esc">
type TekstStiloj = "Tld | SncRef | Klr | Em | Ts | Sup | Sub | Ctl | Mis | Frm | Nom | Nac | Esc"

# <!-- [%priskribaj-elementoj] La unuo <dfn>priskribaj-elementoj</dfn>
# listigas ĉiujn strukturilojn, kiuj priskribas kapvorton aŭ unuopan
# sencon de ĝi. Ĉar ili povas okazi multloke en la strukturo de
# artikolo estas avantaĝe difini tiun ĉi unuon.-->
# <!-- priskribaj elementoj -->
# <!ENTITY % priskribaj-elementoj
#   "fnt|gra|uzo|dif|ekz|rim|ref|refgrp|trd|trdgrp|bld|adm|url|mlg|lstref|tezrad">
type PriskribajElementoj = (
    "Fnt | Gra | Uzo | Dif | Ekz | Rim | Ref | RefGrp | Trd | TrdGrp | Bld | Adm | Url | Mlg | LstRef | TezRad"
)


# <!-- [rad] Radiko de kapvorto. Ĝi estas bezonata por anstaŭigo
# de tildoj. Sekve la "radiko" de afiksoj kaj finaĵoj estu
# ili mem, sen la streketoj antaŭe aŭ malantaŭe.
# La atributo <dfn>var</dfn> povas identigi radikon de variaĵo.
# -->
# <!ELEMENT rad (#PCDATA)>
# <!ATTLIST rad
#        var CDATA #IMPLIED
# >
@dataclasses.dataclass
class Rad(TextOnlyElement):
    """Root of a headword."""

    var: str = ""


# <!-- [ofc] Oficialeco de la kapvorto/derivajho,
#   povas esti *, 1, ..., 8 kiel en PIV -->
# <!ELEMENT ofc (#PCDATA)>
@dataclasses.dataclass
class Ofc(TextOnlyElement):
    """Officiality of a headword or derivation."""


# <!-- [bib] Bibliografia indiko por fonto, estas mallongigo el
# listo de difinitaj bibliografieroj kaj anstataŭas verko- kaj aŭtoroindikon
# en la fontoj.
# -->
# <!ELEMENT bib (#PCDATA)>
@dataclasses.dataclass
class Bib(TextOnlyElement):
    """Short bibilographic reference for a source."""


# <!-- [aut] Aŭtoro de citita frazo aŭ verko -->
# <!ELEMENT aut (#PCDATA)>
@dataclasses.dataclass
class Aut(TextOnlyElement):
    """Author of a phrase or work."""


# <!ELEMENT url (#PCDATA)>
# <!ATTLIST url
#           ref CDATA #IMPLIED>
@dataclasses.dataclass
class Url(TextOnlyElement):
    """A URL."""

    ref: str = ""


# <!-- [lok] Loko, kie troviĝas citita frazo aŭ vorto en verko -->
# <!ELEMENT lok (#PCDATA|url)*>
@dataclasses.dataclass
class Lok(HasTextInContent[Url]):
    """The location of a citation within a work."""


# <!-- [vrk] Verko, en kiu troviĝas citita frazo aŭ vorto -->
# <!ELEMENT vrk (#PCDATA|url)*>
@dataclasses.dataclass
class Vrk(HasTextInContent[Url]):
    """A work containing a citation."""


# <!-- [fnt] Fonto enhavas informojn pri autoro, verko, trovloko
# au aliajn informojn.-->
# <!ELEMENT fnt (#PCDATA|bib|aut|vrk|lok|url)*>
@dataclasses.dataclass
class Fnt(HasTextInContent[Bib | Aut | Vrk | Lok | Url]):
    """A source for a citation."""


# <!-- [tld] Tildo rilatas al la radiko, donita en la kapvorto
# ĝi ne bezonas enhavon. La atributo <dfn>lit</dfn> indikas alian
# komencliteron ol havas la radiko. Grava por majuskligo kaj
# minuskligo. La atributo <dfn>var</dfn> povas identigi radikon de variaĵo.
# -->
# <!ELEMENT tld EMPTY>
# <!ATTLIST tld
#             lit CDATA #IMPLIED
#             var CDATA #IMPLIED
# >
@dataclasses.dataclass
class Tld(Element):
    """The "tilde" replacement for a root."""

    lit: str = ""
    var: str = ""


# <!-- [tezrad] Tezaŭraradiko. La kapvorto aperas en la enir-listo
# de la tezaŭro. Se vi uzas la atributon fak, ĝi aperas en la
# struktura enirlisto de la fako -->
# <!ELEMENT tezrad EMPTY>
# <!ATTLIST tezrad
#         fak CDATA #IMPLIED
# >
@dataclasses.dataclass
class TezRad(Element):
    """A thesaurus root."""

    fak: str = ""


# <!-- [sncref] Referenco al alia senco. Tiu elemento estas anstatauigata
#  per la numero de la referencita senco. Vi povas forlasi la atributon
#  ref, se ekzistas parenca elemento ref, kies atributo cel montras al la
#  referencita senco.
# -->
# <!ELEMENT sncref EMPTY>
# <!ATTLIST sncref
#        ref CDATA #IMPLIED
# >
@dataclasses.dataclass
class SncRef(Element):
    """Reference to another sense of a word."""

    ref: str = ""


# <!-- [g] Grasa parto de formulo, ekz. vektoro, matrico k.s.,
#   bv. uzi nur en frm -->
# <!ELEMENT g (#PCDATA)>
@dataclasses.dataclass
class G(TextOnlyElement):
    """Bold."""


# <!-- [k] Kursiva parto de formulo, ekz. variablo k.s.,
#   bv. uzi nur en frm -->
# <!ELEMENT k (#PCDATA)>
@dataclasses.dataclass
class K(TextOnlyElement):
    """Italic."""


# <!-- [mlg] mallongigo de la kapvorto, ekz. che nomoj de organizajhoj.
# Per "kod" vi povas indiki devenon de la mallongigo, ekz. ISO-3166 ĉe landokodoj -->
# <!ELEMENT mlg (#PCDATA)>
# <!ATTLIST mlg
#           kod CDATA #IMPLIED>
@dataclasses.dataclass
class Mlg(TextOnlyElement):
    """Acronym."""

    kod: str = ""


# <!-- [nom] nomo ne esperantigita, tiuj estas ignorataj dum vortkontrolo  -->
# <!ELEMENT nom (#PCDATA)>
@dataclasses.dataclass
class Nom(TextOnlyElement):
    """A name."""


# <!-- [nac] nacilingva vorto aŭ esprimo, tiuj estas ignorataj dum vortkontrolo  -->
# <!ELEMENT nac (#PCDATA)>
@dataclasses.dataclass
class Nac(TextOnlyElement):
    """A native language word or expression."""


# <!-- [esc] escepte formita (laŭ vidpunkto de vortanalizila gramatiko)
# esperanta vorto aŭ esprimo, tiuj estas ignorataj dum vortkontrolo  -->
# <!ELEMENT esc (#PCDATA)>
@dataclasses.dataclass
class Esc(TextOnlyElement):
    """Exceptional form."""


# <!-- [em] Emfazo. Normale grase skribata vortoj.-->
# <!ELEMENT em (#PCDATA|tld)*>
@dataclasses.dataclass
class Em(HasTextInContent[Tld]):
    """Emphasis."""


# <!-- [ts] trastrekita teksto, ekz-e por montri korekton de misskribita ekzemplo -->
# <!ELEMENT ts (#PCDATA|tld)*>
@dataclasses.dataclass
class Ts(HasTextInContent[Tld]):
    """Strikethrough."""


# <!-- [sup] altigita teksto, ekz. en ĥemiaj formuloj -->
# <!ELEMENT sup (#PCDATA|g|k)*>
@dataclasses.dataclass
class Sup(HasTextInContent[G | K]):
    """Superscript."""


# <!-- [sub] malaltigita teksto, ekz. en ĥemiaj formuloj -->
# <!ELEMENT sub (#PCDATA|g|k)*>
@dataclasses.dataclass
class Sub(HasTextInContent[G | K]):
    """Subscript."""


# <!-- [frm] Matematika au kemia formulo, por matematikaj formuloj oni povas
#     ankaŭ doni esprion laŭ sintakso de AsciiMath por pli bela kompostado -->
# <!ELEMENT frm (#PCDATA|sup|sub|g|k)*>
# <!ATTLIST frm
#           am CDATA #IMPLIED>
@dataclasses.dataclass
class Frm(HasTextInContent[Sup | Sub | G | K]):
    """Mathematical or chemical formula."""

    am: str = ""


# <!-- [uzo] La uzo povas esti stilo, fako, regiono aŭ alia klarigo,
# kiel estas uzata la vorto au termino. Por la fakoj kaj stiloj uzu
# unu el la aliloke listigitaj mallongigoj.
# -->
# <!ELEMENT uzo (#PCDATA|tld)*>
# <!ATTLIST uzo
# 	tip (fak|reg|klr|stl) #IMPLIED
# >
@dataclasses.dataclass
class Uzo(HasTextInContent[Tld]):
    """Field of usage."""

    tip: str = ""


# <!ELEMENT mll (#PCDATA|tld|klr|ind)*>
# <!ATTLIST mll
#         tip (kom|mez|fin) #IMPLIED
# >
@dataclasses.dataclass
class Mll(HasTextInContent["Tld | Klr | Ind"]):
    """An mll element."""

    tip: str = ""


# <!-- [ind] Parto de traduko, kiu liveras la kapvorton en la
# indekso, do &lt;trd&gt;sich &lt;ind&gt;bem&uuml;hen&lt;/ind&gt;&lt;/trd&gt;
# aperas sub bem&uuml;hen. Aŭ parto de ekzemplo aŭ bildpriskribo, al
# kiu rilatas internaj tradukoj ktp.
# -->
# <!ELEMENT ind (#PCDATA|tld|klr|mll)*>
@dataclasses.dataclass
class Ind(HasTextInContent["Tld | Klr | Mll"]):
    """Index."""


# <!-- [trdgrp] Tradukgrupo kunigas diversajn tradukojn de
# sama lingvo.
# -->
# <!ELEMENT trdgrp (#PCDATA|trd)*>
# <!ATTLIST trdgrp
# 	lng CDATA #REQUIRED
# >
@dataclasses.dataclass
class TrdGrp(HasTextInContent["Trd"]):
    """Translation group."""

    lng: str = ""


# <!-- [trd] Traduko konsistas el traduka vorto aŭ frazo
# kaj klarigoj, poste povos sekvi aliaj elementoj.
# Per la atributo <em>fnt</em> oni povas indiki kie
# oni trovis la tradukon.
# La atributo <em>kod</em> estas uzebla por aldoni
# komputile interpreteblan kodon - ni uzas tion por gestolingvo.
# -->
# <!ELEMENT trd (#PCDATA|klr|ind|pr|mll|ofc|baz)*>
# <!ATTLIST trd
# 	lng CDATA #IMPLIED
#         fnt CDATA #IMPLIED
#         kod CDATA #IMPLIED
# >
@dataclasses.dataclass
class Trd(HasTextInContent["Klr | Ind | Pr | Mll | Ofc | Baz"]):
    """Translation."""

    lng: str = ""
    fnt: str = ""
    kod: str = ""


# <!-- [klr] Klarigo pri vorto, difino, ekzemplo ktp.-->
# <!ELEMENT klr (#PCDATA|trd|trdgrp|ekz|ref|refgrp|%tekst-stiloj;)*>
# <!ATTLIST klr
#             tip (ind|amb) #IMPLIED>
@dataclasses.dataclass
class Klr(HasTextInContent["Trd | TrdGrp | Ekz | Ref | RefGrp | TekstStiloj"]):
    """Clarification."""

    tip: str = ""


# <!-- [ref] Referenco montras al alia, simil- aŭ alisignifa vorto,
# oni povas distingi diversajn rilattipon al la
# referencita vorto. La enhavo de la referenco estas tio, kio
# aperas en la legebla teksto. La referencitan vorton mem
# oni difinas per la atributo "cel". La celon oni plej
# bone difinas per: radiko.derivaĵo.difino, oni povas uzi
# la numeron de la difino au derivaĵo. Plej bone oni
# generas la markojn (t.e. la eblaj celoj de referenco)
# aŭtomate por minimumigi erarojn.
# La atributoj "lst" kaj "val" servas por referenci al vortlisto (tip="lst"),
# ekz. monatoj. Se temas pri ordigita listo, vi povas indiki valoron per "val",
# ekz. "3" che la monato marto.
# -->
# <!ELEMENT ref (#PCDATA|tld|klr|sncref)*>
# <!ATTLIST ref
# 	tip (vid|hom|dif|sin|ant|super|sub|prt|malprt|lst|ekz) #IMPLIED
# 	cel CDATA #REQUIRED
#         lst CDATA #IMPLIED
# 	val CDATA #IMPLIED
# >
@dataclasses.dataclass
class Ref(HasTextInContent[Tld | Klr | SncRef]):
    """A reference."""

    tip: str = ""
    cel: str = ""
    lst: str = ""
    val: str = ""


# <!-- [ke] Komunlingva esprimo, per kiu oni povas anstataŭigi la (fakan, tre specialan)
# kapvorton en pli simpla komuna lingvo.
# Tiu esprimo povas konsisti el teksto kaj eventuale enhavi <em>ref</em>erencon. Ĝi
# povas aperi ene de <dfn>dif</dfn>ino, <dfn>rim</dfn>marko kaj referencgrupo
# (<dfn>refgrp</dfn>).
# -->
# <!ELEMENT ke (#PCDATA | ref)*>
@dataclasses.dataclass
class Ke(HasTextInContent[Ref]):
    """Common-language expression."""


# <!-- [refgrp] Referencgrupo grupigas plurajn samtipajn
# referencojn. La tipon indikas la atributo <dfn>tip</dfn>.
# Tiukaze ne uzu la atributon <dfn>tip</dfn> en la subelementoj
# <dfn>ref</dfn>!
# -->
# <!ELEMENT refgrp (#PCDATA|ke|ref)*>
# <!ATTLIST refgrp
# 	tip (vid|hom|dif|sin|ant|super|sub|prt|malprt|lst|ekz) "vid"
# >
@dataclasses.dataclass
class RefGrp(HasTextInContent[Ke | Ref]):
    """Reference group."""

    tip: str = "vid"


# <!-- [ekz] Ekzemplo konsistas el ekzemplofrazo,
# klarigoj kaj fonto.
# -->
# <!ELEMENT ekz (#PCDATA|fnt|uzo|ref|refgrp|ind|trd|trdgrp|%tekst-stiloj;)*>
# <!ATTLIST ekz
# 	mrk ID #IMPLIED
# >
@dataclasses.dataclass
class Ekz(
    HasTextInContent[Fnt | Uzo | Ref | RefGrp | Ind | Trd | TrdGrp | TekstStiloj]
):
    """Example."""

    mrk: str = ""


# <!-- [rim] Rimarko povas enhavi iujn indikojn pri la vorto aŭ
# senco, krome referencojn, ekzemplojn, emfazitajn partojn.
# -->
# <!ELEMENT rim (#PCDATA|ref|refgrp|ke|ekz|aut|fnt|%tekst-stiloj;)*>
# <!ATTLIST rim
#         num CDATA #IMPLIED
# 	mrk ID #IMPLIED
# >
@dataclasses.dataclass
class Rim(HasTextInContent[Ref | RefGrp | Ke | Ekz | Aut | Fnt | TekstStiloj]):
    """Remark."""

    num: str = ""
    mrk: str = ""


# <!-- [var] variaĵo de la vorto, ekz. meĥaniko - mekaniko, pomarbo -
# pomujo. Ĝi povas enhavi fontindikon k.s., sed ankaŭ rimarkojn
# kaj ekzemplojn, sed ĝi ne havas propran difinon. Ĝi aperas ene
# de kapvorto, ĉar ĝi ja estas ĝia variaĵo.
# -->
# <!ELEMENT var (kap,(uzo|klr|ekz|rim)*)>
@dataclasses.dataclass
class Var(HasKap, HasContent[Uzo | Klr | Ekz | Rim]):
    """Variation of a headword."""


# <!-- [vspec] Vortspeco. Ekz. subst. por substantivo; tr./ntr.
# por transitivaj kaj netransitivaj verboj ktp.-->
# <!ELEMENT vspec (#PCDATA)>
@dataclasses.dataclass
class VSpec(TextOnlyElement):
    """Word type."""


# <!-- [gra] kiel grammatikaj informoj momente estas permesataj
# nur indiko de la vortspeco.-->
# <!ELEMENT gra (#PCDATA|vspec)*>
@dataclasses.dataclass
class Gra(HasTextInContent[VSpec]):
    """Grammatical information."""


# <!-- [ctl] citilita teksto, ekz. memindika uzo de vorto -->
# <!ELEMENT ctl (#PCDATA|tld|em|ts|frm|nom|nac|esc)*>
@dataclasses.dataclass
class Ctl(HasTextInContent[Tld | Em | Ts | Frm | Nom | Nac | Esc]):
    """Cited text."""


# <!-- [mis] mislingva teksto, ni prezentos inter asteriskoj -->
# <!ELEMENT mis (#PCDATA|tld|em|ts|frm|nom|nac|esc)*>
@dataclasses.dataclass
class Mis(HasTextInContent[Tld | Em | Ts | Frm | Nom | Nac | Esc]):
    """Ungrammatical text."""


# <!-- [mrk] Per la elemento <dfn>mrk</dfn> oni povas marki lokon en bildo per ia
# kadro, kies pozicio kaj aspekto estas priskribita en la atributo <dfn>stl</dfn>
# per la rimedoj de CSS. Per la atributo <dfn>cel</dfn> oni povas aldoni
# referencon al iu kapvorto de Revo.
# Cetere bildo-marko povas enhavi tekston kaj/aŭ referencojn.
# -->
# <!ELEMENT mrk (#PCDATA | ref)*>
# <!ATTLIST mrk
#   stl CDATA #REQUIRED
#   cel CDATA #IMPLIED
# >
@dataclasses.dataclass
class Mrk(HasTextInContent[Ref]):
    """Marker."""

    stl: str = ""
    cel: str = ""


# <!-- [bld] Bildo povas ilustri iun vorton aŭ sencon. Per la
# atributo <dfn>lok</dfn> ĝi
# referencas al ekstera dosiero, kiu entenas la bildon.
# Per <dfn>alt</dfn> kaj <dfn>lrg</dfn> vi povas doni fiksan formaton.
# Per <dfn>tip</dfn> vi donas tipon de la bildo, t.e. <dfn>img</dfn>
# por JPEG, GIF, PNG-bildo, <dfn>svg</dfn> por SVG-vektorgrafiko.
# Per <dfn>aut</dfn> vi donas aŭtoron kaj <dfn>prm</dfn> la permesilon
# laŭ kiu la bildo rajtas esti uzata (vd ĉe Wikimedia Commons).
# -->
# <!ELEMENT bld (#PCDATA|tld|klr|fnt|mrk|ind|trd|trdgrp)*>
# <!ATTLIST bld
# 	lok CDATA #REQUIRED
# 	mrk ID #IMPLIED
# 	tip (img|svg) "img"
# 	alt CDATA #IMPLIED
# 	lrg CDATA #IMPLIED
#         prm CDATA #IMPLIED
# >
@dataclasses.dataclass
class Bld(HasTextInContent[Tld | Klr | Fnt | Mrk | Ind | Trd | TrdGrp]):
    """Image."""

    lok: str = ""
    mrk: str = ""
    tip: str = "img"
    alt: str = ""
    lrg: str = ""
    prm: str = ""


# <!-- [adm] Administraj informoj estu por redaktado. Ili povus
# enhavi informojn pri kreodato, ŝanĝdato, aŭtoro, eraroj kaj
# plibonigproponoj pri artikolo. Ĝia strukturo ankoraŭ estas
# diskutatebla.
# -->
# <!ELEMENT adm (#PCDATA|aut)*>
@dataclasses.dataclass
class Adm(HasTextInContent[Aut]):
    """Editor's comment."""


# <!-- [pr] Prononco/transskribo, kiel oni uzas por japanaj lingvoj (pinjino, bopomofo, hiragano ks)
# aŭ fonetikaj indikoj de nomoj.
# Se traduko havas transskribon, ni uzos tiun por la indeksado/enordigo en literĉaptiron
# de la indekso. Pro la limigita nombro de literoj/literumaj signoj, tio ebligas
# ĉapitrigi la lingvoindeksojn de silabaj lingvoj. Ankaŭ ni ebligas serĉadon laŭ
# transskribo aldone al la ideografia skribmaniero.
# -->
# <!ELEMENT pr (#PCDATA)>
@dataclasses.dataclass
class Pr(TextOnlyElement):
    """Pronunciation."""


# <!-- [baz] Baza formo de traduko, sub kiu la vorto subordiĝos en la indekso. Tion ni uzas
#   ekzemple en la indonezia indekso, kie sub "ajar" aperas "belajar", "mengajar" ktp.
# -->
# <!ELEMENT baz (#PCDATA)>
@dataclasses.dataclass
class Baz(TextOnlyElement):
    """Base form of a translation."""


# <!-- [lstref] Referenco al vortlisto el artikolo.
# -->
# <!ELEMENT lstref (#PCDATA|tld|klr)*>
# <!ATTLIST lstref
#         lst CDATA #REQUIRED
# >
@dataclasses.dataclass
class LstRef(HasTextInContent[Tld | Klr]):
    """Reference to a word list."""

    lst: str = ""


# <!-- [subsnc] Subsenco ene de senco. Ĝi redonas subtilaĵojn ene de unu senco.
# Ili estas nombrataj per a), b), ... -->
# <!ELEMENT subsnc (%priskribaj-elementoj;)*>
# <!ATTLIST subsnc
# 	mrk ID #IMPLIED
#         ref CDATA #IMPLIED
# >
@dataclasses.dataclass
class SubSnc(HasContent[PriskribajElementoj]):
    """Subsense."""

    mrk: str = ""
    ref: str = ""


# <!-- [snc] Senco de unuopa vorto en artikolo. Komparu la latinajn ciferojn en
# la artikoloj de PIV. Per mrk oni povas referenci sencon de alie. Per ref oni
# referencas al alia senco samartikola (uzata en malmultaj longaj artikoloj, ekz.
# "al". Per num la senco ricevas numeron. Atentu, ke future simbolaj nomoj por
# la sencoj estos perferataj kaj do numerado okazas automate ignorante la atributon
# num. -->
# <!ELEMENT snc (subsnc|%priskribaj-elementoj;)*>
# <!ATTLIST snc
# 	mrk ID #IMPLIED
#         num CDATA #IMPLIED
# 	ref CDATA #IMPLIED
# >
@dataclasses.dataclass
class Snc(HasContent[SubSnc | PriskribajElementoj]):
    """Sense."""

    mrk: str = ""
    num: str = ""
    ref: str = ""


# <!-- [dif] Difino estas la frazo difinanta la vorton, sencon aŭ
# subsencon. Ĝi povas esti ankaŭ en alia(j) lingvo(j) ol la vorto
# mem. La lingvon indikas la atributo <dfn>lng</dfn>.
# -->
# <!ELEMENT dif (#PCDATA|trd|trdgrp|ref|refgrp|ke|ekz|snc|%tekst-stiloj;)*>
# <!ATTLIST dif
# 	lng CDATA #IMPLIED
# >
@dataclasses.dataclass
class Dif(HasTextInContent[Trd | TrdGrp | Ref | RefGrp | Ke | Ekz | Snc | TekstStiloj]):
    """Definition."""

    lng: str = ""


# <!-- [kap] kapvorto okazas en du kuntekstoj - komence de artikolo
# kaj komence de derivaĵo, en la unua kazo ĝi signas radikon
# en la dua kazo ĝi konsistas el iuj literoj kaj eble tildo
# refencanta al la kapvorto, krome en la kapvorto povas okazi
# fontindiko.
# -->
# <!ELEMENT kap (#PCDATA|rad|ofc|fnt|tld|var)*>
@dataclasses.dataclass
class Kap(HasTextInContent[Rad | Ofc | Fnt | Tld | Var]):
    """Headword."""


# <!-- [subdrv] Subderivaĵo. Ĝi grupigas plurajn proksimajn sencojn, se la
# priskribita vorto havas tre multajn sencojn. Tio povas
# rezulti en pli klara strukturo de la artikolo. La subdividaĵoj
# estas nombrataj per A), B), ... -->
# <!ELEMENT subdrv (snc|%priskribaj-elementoj;)*>
# <!ATTLIST subdrv
# 	mrk ID #IMPLIED
# >
@dataclasses.dataclass
class SubDrv(HasContent[Snc | PriskribajElementoj]):
    """Subderivation."""

    mrk: str = ""


# <!-- [drv] Derivaĵo ene de artikolo. Unu artikolo povas priskribi plurajn
# derivaĵojn de la kapvorto. Derivaĵo komenciĝas ja kapvorto kaj
# priskribaj elementoj pri ĝi aŭ el unu aŭ pluraj sencoj aŭ el unu aŭ
# pluraj subdividoj <dfn>subdrv</dfn>.-->
# <!ELEMENT drv (kap,(subdrv|snc|%priskribaj-elementoj;)*)>
# <!ATTLIST drv
# 	mrk ID #REQUIRED
# >
@dataclasses.dataclass
class Drv(HasKap, HasContent[SubDrv | Snc | PriskribajElementoj]):
    """Derivation."""

    mrk: str = ""


# <!-- [subart] Subartikolo. Ĝi povas okazi en <dfn>artikolo</dfn>,
# se la signifoj de vorto (ofte ĉe prepozicioj kaj afiksoj) estas
# tre diversaj. -->
# <!ELEMENT subart (drv|snc|%priskribaj-elementoj;)*>
# <!ATTLIST subart
# 	mrk ID #IMPLIED
# >
@dataclasses.dataclass
class SubArt(HasContent[Drv | Snc | PriskribajElementoj]):
    """Subarticle."""

    mrk: str = ""


# <!-- [art] Unuopa artikolo de la vortaro. Ĝi povas okazi en
# <dfn>vortaro</dfn> (se ne ekzistas precipa-parto),
# <dfn>precipa-parto</dfn>, <dfn>parto</dfn> aŭ <dfn>sekcio</dfn>. Tio
# dependas de la konkreta strukturo de la vortaro. Ĉiu artikolo
# entenas unue kapvorton kaj poste aŭ priskribajn elementojn aŭ plurajn
# derivaĵojn aŭ plurajn sencojn de la kapvorto aŭ subartikolojn. -->
# <!ELEMENT art (kap,(subart|drv|snc|%priskribaj-elementoj;)*)>
# <!ATTLIST art
# 	mrk CDATA #REQUIRED
# >
@dataclasses.dataclass
class Art(HasKap, HasContent[SubArt | Drv | Snc | PriskribajElementoj]):
    """Article."""

    mrk: str = ""


# <!-- [vortaro] Radiko de la strukturarbo de vortaro. La elemento ampleksas
# la tutan vortaron.<p>
# Ĝi entenas aŭ prologon, precipan parton kaj epilogon aŭ plurajn
# artikolojn. Prologo kaj epilogo estas nedevigaj. La ebleco de rekta
# enteno de artikolo ne estas destinita por kompletaj vortaroj, sed por
# eltiroj aŭ unuopa artikolo.-->
# <!ELEMENT vortaro ((prologo?,precipa-parto,epilogo?)|art+)>
# <!--ATTLIST vortaro
#    xmlns CDATA #FIXED "http://steloj.de/voko"
# -->
@dataclasses.dataclass
class Vortaro(HasContent[Art]):
    """Dictionary entry."""


def element_for(qname: str) -> Element:
    """Returns an empty element for the given qname."""
    match qname:
        case "adm":
            return Adm()
        case "art":
            return Art()
        case "aut":
            return Aut()
        case "baz":
            return Baz()
        case "bib":
            return Bib()
        case "bld":
            return Bld()
        case "ctl":
            return Ctl()
        case "dif":
            return Dif()
        case "drv":
            return Drv()
        case "ekz":
            return Ekz()
        case "em":
            return Em()
        case "esc":
            return Esc()
        case "fnt":
            return Fnt()
        case "frm":
            return Frm()
        case "g":
            return G()
        case "gra":
            return Gra()
        case "ind":
            return Ind()
        case "k":
            return K()
        case "kap":
            return Kap()
        case "ke":
            return Ke()
        case "klr":
            return Klr()
        case "lok":
            return Lok()
        case "lstref":
            return LstRef()
        case "mis":
            return Mis()
        case "mlg":
            return Mlg()
        case "mrk":
            return Mrk()
        case "nac":
            return Nac()
        case "nom":
            return Nom()
        case "ofc":
            return Ofc()
        case "pr":
            return Pr()
        case "rad":
            return Rad()
        case "ref":
            return Ref()
        case "refgrp":
            return RefGrp()
        case "rim":
            return Rim()
        case "snc":
            return Snc()
        case "sncref":
            return SncRef()
        case "sub":
            return Sub()
        case "sup":
            return Sup()
        case "tezrad":
            return TezRad()
        case "tld":
            return Tld()
        case "trd":
            return Trd()
        case "trdgrp":
            return TrdGrp()
        case "ts":
            return Ts()
        case "url":
            return Url()
        case "uzo":
            return Uzo()
        case "var":
            return Var()
        case "vortaro":
            return Vortaro()
        case "vrk":
            return Vrk()
        case "vspec":
            return VSpec()
        case _:
            raise ValueError(f"Unknown element: {qname}")

ELEMENT_TYPES: dict[str, type] = {
    # Keep elements sorted
    "adm": Adm,
    "art": Art,
    "aut": Aut,
    "baz": Baz,
    "bib": Bib,
    "bld": Bld,
    "ctl": Ctl,
    "dif": Dif,
    "drv": Drv,
    "ekz": Ekz,
    "em": Em,
    "esc": Esc,
    "fnt": Fnt,
    "frm": Frm,
    "g": G,
    "gra": Gra,
    "ind": Ind,
    "k": K,
    "kap": Kap,
    "ke": Ke,
    "klr": Klr,
    "lok": Lok,
    "lstref": LstRef,
    "mis": Mis,
    "mlg": Mlg,
    "mll": Mll,
    "mrk": Mrk,
    "nac": Nac,
    "nom": Nom,
    "ofc": Ofc,
    "pr": Pr,
    "rad": Rad,
    "ref": Ref,
    "refgrp": RefGrp,
    "rim": Rim,
    "snc": Snc,
    "sncref": SncRef,
    "sub": Sub,
    "subart": SubArt,
    "subdrv": SubDrv,
    "subsnc": SubSnc,
    "sup": Sup,
    "tezrad": TezRad,
    "tld": Tld,
    "trd": Trd,
    "trdgrp": TrdGrp,
    "ts": Ts,
    "url": Url,
    "uzo": Uzo,
    "var": Var,
    "vortaro": Vortaro,
    "vrk": Vrk,
    "vspec": VSpec,
}
