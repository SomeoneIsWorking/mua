#include "mua/title_profile.hpp"

#include "mua_profile_data.hpp"

namespace mua
{

const TitleProfile& GoldProfile() noexcept
{
    static constexpr TitleProfile Profile = {
        .name = generated::Name,
        .title_id = generated::TitleId,
        .media_id = generated::MediaId,
        .disc_sha256 = generated::DiscSha256,
        .xex_sha256 = generated::XexSha256,
        .image =
            {
                .sha256 = generated::ImageSha256,
                .base = generated::ImageBase,
                .size = generated::ImageSize,
                .entry_point = generated::EntryPoint,
            },
    };
    return Profile;
}

} // namespace mua
