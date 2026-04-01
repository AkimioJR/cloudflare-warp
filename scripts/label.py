from enum import Enum


class Distro(Enum):
    # Ubuntu
    NOBLE = "noble"
    JAMMY = "jammy"
    FOCAL = "focal"

    # Ubuntu (legacy)
    BIONIC = "bionic"
    XENIAL = "xenial"

    # Debian
    TRIXIE = "trixie"
    BOOKWORM = "bookworm"
    BULLSEYE = "bullseye"

    # Debian (legacy)
    BUSTER = "buster"
    STRETCH = "stretch"

    default = NOBLE

    @classmethod
    def allCases(cls, only_supported: bool = False) -> list["Distro"]:
        """
        allCases returns a list of all Distro enum members
        :param only_supported: if True, only return supported distros
        """
        if only_supported:
            return [
                cls.NOBLE,
                cls.JAMMY,
                cls.FOCAL,
                cls.TRIXIE,
                cls.BOOKWORM,
                cls.BULLSEYE,
            ]
        return [
            cls.NOBLE,
            cls.JAMMY,
            cls.FOCAL,
            cls.BIONIC,
            cls.XENIAL,
            cls.TRIXIE,
            cls.BOOKWORM,
            cls.BULLSEYE,
            cls.BUSTER,
            cls.STRETCH,
        ]

    @property
    def label(self) -> str:
        DISTRO_MAP: dict[Distro, str] = {
            Distro.NOBLE: "Ubuntu Noble (24.04)",
            Distro.JAMMY: "Ubuntu Jammy (22.04)",
            Distro.FOCAL: "Ubuntu Focal (20.04)",
            Distro.BIONIC: "Ubuntu Bionic (18.04)",
            Distro.XENIAL: "Ubuntu Xenial (16.04)",
            Distro.TRIXIE: "Debian Trixie (13)",
            Distro.BOOKWORM: "Debian Bookworm (12)",
            Distro.BULLSEYE: "Debian Bullseye (11)",
            Distro.BUSTER: "Debian Buster (10)",
            Distro.STRETCH: "Debian Stretch (9)",
        }

        return DISTRO_MAP.get(self, self.value)


class Arch(Enum):
    AMD64 = "amd64"
    ARM64 = "arm64"

    default = AMD64

    @classmethod
    def allCases(cls) -> list["Arch"]:
        """
        allCases returns a list of all Arch enum members
        """
        return [cls.AMD64, cls.ARM64]
