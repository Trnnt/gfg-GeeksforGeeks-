class Solution {
  public:
    int arraySum(vector<int>& arr) {
        // code here
        int ans=0;
        for(int i =0; i<arr.size(); i++){
            ans += arr[i];
            continue;
        }
        return ans;
    }
};