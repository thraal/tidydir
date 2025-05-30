"""File category definitions and extension mappings."""

from enum import Enum
from typing import Dict, Set


class FileCategory(str, Enum):
    """Enumeration of file categories."""
    
    APPLICATIONS = "Applications"
    ARCHIVES = "Archives"
    DOCUMENTS = "Documents"
    FONTS = "Fonts"
    IMAGES = "Images"
    SCRIPTS = "Scripts"
    TEXT = "Text"
    VIDEOS = "Videos"
    THREE_D = "3D"
    DISK_IMAGES = "Disk Images"
    VMS = "VMs"
    AUDIO = "Audio"
    EBOOKS = "Ebooks"
    SPREADSHEETS = "Spreadsheets"
    PRESENTATIONS = "Presentations"
    CODE = "Code"
    FILES = "Files"  # Default category


# File extension mappings to categories
CATEGORY_EXTENSIONS: Dict[FileCategory, Set[str]] = {
    FileCategory.APPLICATIONS: {
        '.exe', '.msi', '.app', '.deb', '.rpm', '.dmg', '.pkg', '.appimage',
        '.apk', '.ipa', '.xpi', '.vsix'
    },
    FileCategory.ARCHIVES: {
        '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.xz', '.tgz', '.tar.gz',
        '.tar.bz2', '.tar.xz', '.cab', '.arj', '.z', '.lz', '.lzma', '.lzo',
        '.rz', '.sz', '.dz'
    },
    FileCategory.DOCUMENTS: {
        '.pdf', '.doc', '.docx', '.odt', '.rtf', '.tex', '.wpd', '.wps',
        '.pages', '.key', '.odp', '.ods', '.odf', '.xps', '.ps', '.eps',
        '.prn', '.dvi'
    },
    FileCategory.FONTS: {
        '.ttf', '.otf', '.woff', '.woff2', '.eot', '.fon', '.fnt', '.ttc',
        '.pfb', '.pfm', '.afm', '.sfd', '.vlw'
    },
    FileCategory.IMAGES: {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.tiff',
        '.webp', '.psd', '.xcf', '.raw', '.heif', '.heic', '.dng', '.cr2',
        '.nef', '.arw', '.orf', '.rw2', '.pef', '.sr2', '.raf', '.mrw',
        '.dcr', '.mos', '.nrw', '.ptx', '.pxn', '.r3d', '.x3f', '.srw',
        '.tga', '.dds', '.jfif', '.jp2', '.jpx', '.pbm', '.pgm', '.ppm',
        '.pnm', '.mng', '.apng', '.clip', '.cpt', '.exr', '.hdr', '.picti',
        '.sct', '.sgi', '.targa', '.vicar', '.viff', '.cur', '.ani'
    },
    FileCategory.SCRIPTS: {
        '.py', '.js', '.sh', '.bat', '.ps1', '.rb', '.pl', '.php', '.bash',
        '.zsh', '.fish', '.ksh', '.csh', '.tcsh', '.awk', '.sed', '.lua',
        '.tcl', '.r', '.m', '.ahk', '.au3', '.applescript', '.vbs', '.cmd',
        '.psm1', '.psd1', '.ps1xml'
    },
    FileCategory.TEXT: {
        '.txt', '.md', '.log', '.csv', '.json', '.xml', '.yaml', '.yml',
        '.ini', '.cfg', '.conf', '.properties', '.toml', '.rst', '.tex',
        '.adoc', '.textile', '.creole', '.mediawiki', '.wiki', '.nfo',
        '.readme', '.asc', '.etx', '.irclog', '.man', '.me', '.plain',
        '.rpt', '.ans', '.ascii', '.diz', '.ezt', '.info', '.lit', '.lnt',
        '.text', '.strings', '.vtt', '.srt', '.sub', '.sbv', '.ssa', '.ass'
    },
    FileCategory.VIDEOS: {
        '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v',
        '.mpg', '.mpeg', '.3gp', '.3g2', '.f4v', '.f4p', '.ogv', '.ogg',
        '.drc', '.mng', '.qt', '.yuv', '.rm', '.rmvb', '.asf', '.amv',
        '.m2v', '.svi', '.mxf', '.roq', '.nsv', '.f4a', '.f4b', '.m2ts',
        '.mts', '.vob', '.dv', '.mj2', '.mjpeg', '.m1v', '.m2p', '.m2t',
        '.m4p', '.minipsf', '.nut', '.bik', '.smk', '.viv', '.daf', '.divx',
        '.evo', '.mk3d', '.ivf', '.mpe', '.mpv', '.mpv2', '.m1v', '.m2v',
        '.fli', '.flc', '.fxm', '.emf', '.ts', '.tsv', '.tsa', '.m2ts',
        '.m2t', '.camrec', '.dav', '.wtv', '.ssif', '.smv', '.rv', '.dvr-ms',
        '.mswmm', '.mseq', '.seq', '.clpi', '.rec', '.bdm', '.bdmv'
    },
    FileCategory.THREE_D: {
        '.obj', '.fbx', '.dae', '.3ds', '.blend', '.stl', '.ply', '.gltf',
        '.glb', '.usdz', '.x3d', '.x3db', '.bvh', '.dxf', '.lwo', '.lws',
        '.m3d', '.md2', '.md3', '.md5', '.mesh', '.mot', '.ms3d', '.nif',
        '.off', '.ogex', '.q3d', '.q3s', '.raw', '.smd', '.u3d', '.vrml',
        '.wrl', '.x', '.xgl', '.zgl', '.3dm', '.max', '.3dxml', '.x3dz',
        '.x3dbz', '.x3dv', '.x3dvz', '.x3db', '.c4d', '.lxo', '.ma', '.mb',
        '.jas', '.mdl', '.wire', '.stl', '.iges', '.igs', '.step', '.stp'
    },
    FileCategory.DISK_IMAGES: {
        '.iso', '.img', '.vhd', '.vhdx', '.vdi', '.vmdk', '.dmg', '.cdr',
        '.dvd', '.wim', '.swm', '.esd', '.nrg', '.mdf', '.mds', '.mdx',
        '.ccd', '.sub', '.ima', '.udf', '.bin', '.cue', '.daa', '.pxi',
        '.nri', '.isz', '.eui', '.vcd', '.bwt', '.cdi', '.b5t', '.b6t',
        '.bwi', '.bws', '.bwa', '.ape', '.flac', '.wv', '.sdi', '.mde',
        '.md0', '.md1', '.md2', '.xa', '.ede', '.eds', '.ddi', '.gbi',
        '.tib', '.vbox-extpack'
    },
    FileCategory.VMS: {
        '.ova', '.ovf', '.vbox', '.vbox-prev', '.vmc', '.vmwarevm', '.vmx',
        '.vmxf', '.vmsd', '.vmsn', '.vmss', '.nvram', '.vmem', '.vmtm',
        '.vmt', '.vhd', '.vhdx', '.avhd', '.avhdx', '.vud', '.vdi', '.hdd',
        '.pvs', '.sav', '.xva', '.qcow', '.qcow2', '.qed', '.vhdp'
    },
    FileCategory.AUDIO: {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus',
        '.ape', '.mka', '.au', '.aiff', '.aif', '.aifc', '.dts', '.dtshd',
        '.ac3', '.amr', '.awb', '.dss', '.dvf', '.m4b', '.m4p', '.mmf',
        '.mpc', '.msv', '.oga', '.mogg', '.ra', '.rm', '.raw', '.sln',
        '.tta', '.voc', '.vox', '.wv', '.webm', '.8svx', '.cda', '.mid',
        '.midi', '.mus', '.sib', '.sid', '.xm', '.it', '.s3m', '.mod',
        '.mtm', '.umx', '.vgm', '.vgz', '.aac', '.alac', '.mlp', '.dsd',
        '.dsf', '.dff', '.tak', '.thd', '.tta', '.caf', '.kar', '.snd',
        '.vqf', '.spx', '.spc', '.gym', '.adx', '.dsp', '.adp', '.ymf',
        '.ast', '.afc', '.ymf', '.lwav', '.smp', '.aud', '.sng', '.imf',
        '.m15', '.ply', '.m3u', '.m3u8', '.pls', '.asx', '.xspf'
    },
    FileCategory.EBOOKS: {
        '.epub', '.mobi', '.azw', '.azw3', '.fb2', '.lit', '.pdb', '.kf8',
        '.azw4', '.tpz', '.prc', '.tcr', '.snb', '.webz', '.txtz', '.htmlz',
        '.oeb', '.lrf', '.lrx', '.cbr', '.cbz', '.cbt', '.cba', '.cb7',
        '.djvu', '.ibooks', '.oxps', '.xps', '.fb3', '.kfx', '.acsm', '.mart',
        '.mbp', '.ybk', '.koob', '.eal', '.ebk', '.ebx', '.etd', '.hsb',
        '.lit', '.lrs', '.nat', '.ncx', '.odb', '.odf', '.odm', '.odt',
        '.opu', '.opf', '.pef', '.phl', '.prc', '.rzb', '.rzs', '.tcz',
        '.tr', '.tr3', '.xeb', '.ava', '.bkk', '.brn', '.ceb', '.dnl',
        '.edn', '.eit', '.ebm', '.ebo', '.ebr', '.ebs', '.ebx', '.ecw',
        '.emd', '.emo', '.eny', '.eot', '.eta', '.etx', '.evi', '.evy',
        '.fax', '.fcf', '.fdr', '.fds', '.fdt', '.fdx', '.fft', '.fha',
        '.fhd', '.fhf', '.fik', '.fkb', '.fub', '.gho', '.gpd', '.han',
        '.hbk', '.htz', '.htx', '.htz4', '.htz5', '.htx', '.hux', '.hvx',
        '.hya', '.hyb', '.isx', '.jbr', '.jcr', '.kdz', '.keb', '.key',
        '.kfn', '.kfx', '.kml', '.kne', '.kon', '.kpf', '.kpw', '.lbr',
        '.lbxcol', '.lbxoeb', '.lbxosh', '.ldo', '.lix', '.llb', '.lrs',
        '.lrt', '.lrv', '.lrx', '.ltr', '.lts', '.ltz', '.lza', '.mag',
        '.mbp', '.meb', '.mht', '.mpub', '.msg', '.mwp', '.nfx', '.nva',
        '.obb', '.obk', '.obo', '.odc', '.odg', '.odi', '.odp', '.ods',
        '.odt', '.oeb', '.oebzip', '.onb', '.oop', '.opz', '.orn', '.orv',
        '.osi', '.otb', '.ott', '.otu', '.otz', '.oux', '.ove', '.ovx',
        '.owb', '.owc', '.oxb', '.p7a', '.p7s', '.pck', '.pcz', '.pdb',
        '.pdg', '.pdz', '.pea', '.peb', '.pec', '.pef', '.pex', '.pez',
        '.pfg', '.pfr', '.pk', '.pkg', '.plb', '.plc', '.pld', '.plf',
        '.pli', '.plx', '.pma', '.pmd', '.pml', '.pmlz', '.pmn', '.pmo',
        '.pmr', '.pmu', '.pmx', '.pmz', '.pnc', '.pnz', '.pot', '.ppa',
        '.ppb', '.ppn', '.ppo', '.ppp', '.ppw', '.ppx', '.pqa', '.pqb'
    },
    FileCategory.SPREADSHEETS: {
        '.xls', '.xlsx', '.ods', '.xlsm', '.xlsb', '.xltx', '.xltm', '.csv',
        '.tsv', '.dif', '.dbf', '.prn', '.slk', '.gnumeric', '.numbers',
        '.et', '.wks', '.wk1', '.wk2', '.wk3', '.wk4', '.xlr', '.xlt',
        '.xlam', '.xla', '.xlw', '.xlc', '.ots', '.sxc', '.stc', '.fods',
        '.wq1', '.wq2', '.wks', '.wku', '.dex', '.px'
    },
    FileCategory.PRESENTATIONS: {
        '.ppt', '.pptx', '.odp', '.pps', '.ppsx', '.pptm', '.ppsm', '.potx',
        '.potm', '.pot', '.otp', '.sxi', '.sti', '.pez', '.prz', '.shw',
        '.show', '.slp', '.sspss', '.ope', '.sdd', '.sdp', '.sdd', '.sdw',
        '.sgl', '.sor', '.sxd', '.sxg', '.sxi', '.sxm', '.sxw', '.uop',
        '.vor', '.vsd', '.vss', '.vst', '.vdx', '.vsx', '.vtx', '.vsw',
        '.vsdx', '.vssx', '.vstx', '.vsdm', '.vssm', '.vstm', '.gslides',
        '.fodp', '.sldx', '.sldm'
    },
    FileCategory.CODE: {
        '.c', '.cpp', '.h', '.hpp', '.cc', '.cxx', '.c++', '.hh', '.hxx',
        '.h++', '.cp', '.tcc', '.inl', '.ipp', '.def', '.odl', '.idl',
        '.rc', '.rc2', '.rct', '.rgs', '.r', '.rd', '.rsx', '.fx', '.fxh',
        '.hlsl', '.vsh', '.psh', '.cg', '.shd', '.glsl', '.shader', '.java',
        '.class', '.jar', '.groovy', '.scala', '.clj', '.cljs', '.cljc',
        '.edn', '.kt', '.kts', '.dart', '.cs', '.csx', '.vb', '.vbs',
        '.bas', '.frm', '.cls', '.ctl', '.pag', '.dsr', '.dob', '.vbhtml',
        '.vbproj', '.vbproj.user', '.sln', '.csproj', '.fs', '.fsi', '.ml',
        '.mli', '.fsx', '.fsscript', '.pas', '.pp', '.inc', '.lpr', '.lfm',
        '.dpr', '.dpk', '.dproj', '.groupproj', '.bdsgroup', '.bdsproj',
        '.bpr', '.dfm', '.nfm', '.xfm', '.fmx', '.res', '.chr', '.rs',
        '.rlib', '.so', '.dll', '.dylib', '.a', '.lib', '.la', '.lo',
        '.exp', '.pdb', '.idb', '.ilk', '.manifest', '.dep',
        '.iobj', '.ipdb', '.pch', '.gch', '.pchi', '.hdmp', '.ncb',
        '.aps', '.sbr', '.bsc', '.fd', '.fe', '.tlog', '.lastbuildstate',
        '.meta', '.obj', '.pgc', '.pgd', '.rsp', '.tli',
        '.tlh', '.tmp', '.tmp_proj', '.vspscc', '.vssscc', '.builds',
        '.pidb', '.svclog', '.scc', '.vcxproj', '.vcxproj.filters',
        '.vcxproj.user', '.vcproj', '.vdproj', '.dbproj', '.dbproj.user',
        '.go', '.s', '.S', '.asm', '.nasm', '.yasm', '.swift', '.playground',
        '.m', '.mm', '.M', '.d', '.di', '.dd', '.ddoc',
        '.map', '.pc', '.pod', '.rst', '.hs',
        '.lhs', '.hi', '.hc', '.cabal', '.erl', '.hrl', '.beam', '.app',
        '.yrl', '.xrl', '.ex', '.exs', '.eex', '.jl', '.nim', '.nims',
        '.nimble', '.zig', '.v', '.vh', '.sv', '.svh', '.vhd', '.vhdl',
        '.vho', '.vhs', '.vht', '.vhw', '.vhc', '.ucf', '.qsf', '.tcl',
        '.sdc', '.xdc', '.xise', '.gise', '.ise', '.xmp', '.xco', '.ngc',
        '.ngo', '.asy', '.prj', '.psl', '.rpt', '.veo', '.vmo',
        '.syr', '.par', '.pad', '.unroutes', '.xpi', '.xst',
        '.stx', '.ngm', '.mrp', '.xrpt', '.drc', '.bgn', '.bit', '.xwbt', '.ngd', '.bld', '.ncd', '.ngr',
        '.pcf', '.auto', '.trace', '.twr', '.twx',
        '.cmd_log', '.jhd', '.ant', '.gradle', '.mvn', '.ivy',
        '.project', '.classpath', '.settings', '.idea', '.iml', '.ipr',
        '.iws', '.pro', '.pri', '.cmake', '.ninja', '.mk', '.makefile',
        '.gnumakefile', '.rules', '.ninja_deps', '.ninja_log', '.bazel',
        '.bzl', '.BUILD', '.WORKSPACE', '.gn', '.gni', '.gyp', '.gypi'
    }
}
