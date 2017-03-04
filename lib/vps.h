#ifndef vps_h
#define vps_h

typedef struct messagePoint__xxx {

  int level;
  void *fnptr;
  void *target;

} vps__messagePoint;

extern void vps__send(vps__messagePoint mp, void* params);

#endif
