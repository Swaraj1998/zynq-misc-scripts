import os
import sys
import mmap

def read(addr, num_bytes):
    base = addr & 0xfffff000
    fd = os.open('/dev/mem', os.O_RDWR | os.O_SYNC)
    mm = mmap.mmap(fd, addr - base + 4, mmap.MAP_SHARED,
            mmap.PROT_READ | mmap.PROT_WRITE, offset=base) 
    mm.seek(addr - base)
    val = int.from_bytes(mm.read(num_bytes), 'little')
    os.close(fd)
    return val

def write(addr, num_bytes, val):
    base = addr & 0xfffff000
    fd = os.open('/dev/mem', os.O_RDWR | os.O_SYNC)
    mm = mmap.mmap(fd, addr - base + 4, mmap.MAP_SHARED,
            mmap.PROT_READ | mmap.PROT_WRITE, offset=base) 
    mm.seek(addr - base)
    mm.write(val.to_bytes(num_bytes, 'little'))
    os.close(fd)

def ftm_enable():
    XDCFG_CTRL_REG = 0xf8007000
    XDCFG_CTRL_SPIDEN_MASK = (1 << 5)
    FTM_GLB_CTRL = 0xf880b000

    write(FTM_GLB_CTRL, 1, 0x01)

    ctrl = read(XDCFG_CTRL_REG, 4)
    #print(hex(ctrl))
    write(XDCFG_CTRL_REG, 4, ctrl | XDCFG_CTRL_SPIDEN_MASK)

def dbg_unlock():
    XDCFG_LOCK_REG = 0xf8007004
    XDCFG_LOCK_DBG_MASK = (1 << 0)

    lock = read(XDCFG_LOCK_REG, 4)
    #print(hex(lock))
    write(XDCFG_LOCK_REG, 4, lock & ~XDCFG_LOCK_DBG_MASK) 


if __name__ == "__main__":
    assert len(sys.argv) >= 2

    dbg_unlock()
    ftm_enable()

    # Unlock write access to FTM
    write(0xf880bfb0, 4, 0xc5acce55)

    if sys.argv[1][:3] == 'p2f':
        assert len(sys.argv) == 3
        reg = int(sys.argv[1][3])
        if reg == 0:
            write(0xf880b00c, 1, int(sys.argv[2], 16))
        elif reg == 1:
            write(0xf880b010, 1, int(sys.argv[2], 16))
        elif reg == 2:
            write(0xf880b014, 1, int(sys.argv[2], 16))
        elif reg == 3:
            write(0xf880b018, 1, int(sys.argv[2], 16))
        else:
            print('Invalid register!')

    elif sys.argv[1] == 'f2p':
        val = read(0xf880b01c, 1)
        val |= read(0xf880b020, 1) << 8
        val |= read(0xf880b024, 1) << 16
        val |= read(0xf880b028, 1) << 24
        print('0x{:08x}'.format(val))

    elif sys.argv[1][:3] == 'f2p':
        reg = int(sys.argv[1][3])
        if reg == 0:
            val = read(0xf880b01c, 1)
        elif reg == 1:
            val = read(0xf880b020, 1)
        elif reg == 2:
            val = read(0xf880b024, 1)
        elif reg == 3:
            val = read(0xf880b028, 1)
        else:
            print('Invalid register!')
        print(hex(val))

    else:
        print('Invalid option!')
