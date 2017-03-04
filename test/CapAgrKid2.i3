CAPSULE INTERFACE CapAgrKid2 ;
IMPORT CapAgrTypes AS CAT;
PORT p1 : CAT.wholeLoad;
PORT p2 : ~ (CAT.start @ CAT.middle @ PROTOCOL INCOMING MESSAGE endMsg (); END);
END CapAgrKid2.
