user = User.find_by_username('root')
token_name = 'AnsibleAutomation'
target_token = '{{ gitlab_root_token }}'

# This script only runs when the token was not accepted: drop the old one
user.personal_access_tokens.where(name: token_name).each do |old_token|
  puts 'Deleting old token'
  old_token.destroy!
end

puts 'Create new token'
new_token = user.personal_access_tokens.create!(
  scopes: Gitlab::Auth.all_available_scopes,
  name: token_name,
  expires_at: 365.days.from_now
)
new_token.set_token(target_token)
new_token.save!
puts 'Token successfully created'
