#ifndef MUA_TITLE_PROFILE_HPP
#define MUA_TITLE_PROFILE_HPP

#include "xenon_host/guest_module.hpp"

#include <cstdint>
#include <string_view>

namespace mua
{

struct TitleProfile
{
    std::string_view name;
    std::uint32_t title_id;
    std::uint32_t media_id;
    xenon_host::Sha256Digest disc_sha256;
    xenon_host::Sha256Digest xex_sha256;
    xenon_host::ImageIdentity image;
};

[[nodiscard]] const TitleProfile& GoldProfile() noexcept;

} // namespace mua

#endif
