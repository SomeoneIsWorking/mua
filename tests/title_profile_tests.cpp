#include "mua/title_profile.hpp"

#include <algorithm>
#include <cstdint>
#include <cstdio>

namespace
{

bool Nonzero(const xenon_host::Sha256Digest& digest)
{
    return std::ranges::any_of(digest, [](std::uint8_t byte) { return byte != 0; });
}

} // namespace

int main()
{
    const mua::TitleProfile& profile = mua::GoldProfile();
    const std::uint64_t image_end =
        static_cast<std::uint64_t>(profile.image.base) + profile.image.size;
    const bool valid = !profile.name.empty() && profile.title_id != 0 && profile.media_id != 0 &&
                       Nonzero(profile.disc_sha256) && Nonzero(profile.xex_sha256) &&
                       Nonzero(profile.image.sha256) && profile.image.size != 0 &&
                       (profile.image.base & 3U) == 0 && (profile.image.entry_point & 3U) == 0 &&
                       profile.image.entry_point >= profile.image.base &&
                       profile.image.entry_point < image_end && image_end <= 0x100000000ULL;
    if (!valid)
    {
        std::fprintf(stderr, "MUA Gold profile violates the title/module identity contract\n");
        return 1;
    }
    std::printf("MUA Gold profile contract: title=%08x media=%08x image=%08x+%08x entry=%08x\n",
                profile.title_id, profile.media_id, profile.image.base, profile.image.size,
                profile.image.entry_point);
    return 0;
}
