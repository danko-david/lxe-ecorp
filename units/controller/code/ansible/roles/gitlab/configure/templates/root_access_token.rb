user = User.find_by_username('root')
token_name = 'AnsibleAutomation'
target_token = 'SUPER_SECRET_ROOT_TOKEN'

# find existing token by name
existing_token = user.personal_access_tokens.find_by(name: token_name)

# If exists but expires in 7 days renew
if existing_token && existing_token.expires_at < 7.days.from_now
  puts 'Token is about to expire, deleting'
  existing_token.destroy!
  existing_token = nil
end

# Create new token
if existing_token.nil?
  puts 'Create new token'
  new_token = user.personal_access_tokens.create!(
    scopes: Gitlab::Auth.all_available_scopes, 
    name: token_name, 
    expires_at: 365.days.from_now
  )
  new_token.set_token(target_token)
  new_token.save!
  puts 'Token successfully created'
else
  puts 'Token is valid Nothing to do'
end
